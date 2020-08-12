from Hand import Hand
import valid_data


class Player:
    action = ('STAND', 'HIT', 'DOUBLE DOWN', 'SPLIT')

    def __init__(self, *args):
        name, cash = args

        self.__name = name
        self.__hands = []  # List[Hand]
        self.__cmd = list(Player.action)

        self.__cash = cash
        self.__bet = 0

    def __str__(self):
        out_str = "%-15s " % self.__name

        if self.__name != "DEALER":
            out_str += " cash/bet: %7.2f /  %7.2f $" % (self.__cash, self.__bet)
            out_str += "     ["

            len_hands = len(self.__hands)
            for index in range(len_hands):
                out_str += str(self.__hands[index])
                if index < len_hands - 1:
                    out_str += " | "

            out_str += "]"
        else:
            # DEALER HANDS
            for hand in self.__hands:
                out_str += str(hand)

        return out_str

    def get_hand(self, cards):
        if self.__name == 'DEALER' and len(self.__hands) == 0:
            self.__hands.append(Hand(cards))
            self.__hands[0].dealer_hand()
        else:
            self.__hands.append(Hand(cards))
            last = len(self.__hands) - 1
            self.__hands[last].player_hand()

        # split cmd reduction
        if not self.has_split():
            self.__cmd = ['STAND', 'HIT', 'DOUBLE DOWN']

    def uncover_dealer(self, deck):
        self.__hands[0].player_hand()
        while len(self.__hands[0]) < 17:
            self.__hands[0].push_card(deck.draw_card())
        return len(self.__hands[0])

    # ACTIONS
    def hit(self, deck):
        self.__hands[0].push_card(deck.draw_card())
        print(self)
        ask_str = "Hit again [y/n]?"
        for index in range(len(self.__hands)):
            hand = self.__hands[0]
            str_index = ask_str
            if index > 0:
                str_index += ':' + str(index)

            while not hand.is_busted() and 'y' == valid_data.yn_input(str_index):
                self.__hands[index].push_card(deck.draw_card())
                hand = self.__hands[index]
                print(self)

        self.__cmd = []

    def split(self, deck):
        if self.has_split():

            [new_card1, new_card2] = deck.draw_card(2)

            last_card = self.__hands[0].pop_card()
            self.__hands[0].push_card(new_card1)
            self.get_hand([last_card, new_card2])

            self.__cmd = ['STAND', 'HIT', 'DOUBLE DOWN']
            self.bet_up()
            return True
        else:
            print("[Can't make 'SPLIT' ]")
            return False

    def double_down(self, deck):
        for hand in self.__hands:
            hand.push_card(deck.draw_card())

        self.bet_up()
        self.__cmd = []

    def has_split(self):
        hands = self.__hands
        return len(hands) == 1 and hands[0].is_split()

    def __show_action(self):
        """
            0 - STAND
            1 - HIT
            2 - DD
            3 - SPLIT
        """
        for act in range(len(self.__cmd)):
            print(act, self.__cmd[act])

    def make_action(self, deck):
        while len(self.__cmd) > 0:
            print()
            print(self)
            self.__show_action()
            ans = valid_data.int_input(self.__name + " choose option: ", len(self.__cmd)-1,0)
            cmd = self.__cmd[ans]
            if 'STAND' == cmd:
                self.__cmd = []
            elif 'HIT' == cmd:
                self.hit(deck)
            elif 'DOUBLE DOWN' == cmd:
                self.double_down(deck)
            elif 'SPLIT' == cmd:
                self.split(deck)

    def declare_bet(self, small_blind):
        print(self.__name, "is now declaring | cash:", self.__cash)
        if self.__cash >= small_blind:
            bet = valid_data.float_input("Declare a bet: ", self.__cash, small_blind)
            self.__cash -= bet
            self.__bet += bet
            return bet
        else:
            return 0.

    def bet_up(self):
        if self.__bet > self.__cash:
            self.__bet += self.__cash
            self.__cash = 0
        else:
            self.__cash -= self.__bet
            self.__bet *= 2

    # after game
    def collect_cards(self, deck):
        for hand in self.__hands:
            count = hand.how_many()
            for idx in range(count):
                deck.push_cards(hand.pop_card())

        self.__cmd = list(Player.action)

    def payoff(self, dealer_pts):
        piles = len(self.__hands)
        self.__bet *= 2
        self.__bet /= piles
        for hand in self.__hands:
            if Player.win_condition(len(hand), dealer_pts):
                self.__cash += self.__bet
        self.__bet = 0

    @staticmethod
    def win_condition(hand, deal_pts):
        return deal_pts > 21 >= hand or hand == 21 or 21 > hand > deal_pts

