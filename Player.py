from Hand import Hand
import valid_data


class Player:
    action = ('SURRENDER', 'STAND', 'HIT', 'DOUBLE DOWN', 'SPLIT')

    def __init__(self, *args):
        name, cash = args

        self.__name = name
        self.__hands = []  # List[Hand]

        self.__cash = cash
        self.__bet = 0

    def __str__(self):
        out_str = "%-15s " % self.__name

        if self.__name != "DEALER":
            out_str += " cash/bet:   %5.2f /   %5.2f $" % (self.__cash, self.__bet)
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
        if self.__name == 'DEALER':
            self.__hands.append(Hand(cards))
            self.__hands[0].dealer_hand()
        else:
            self.__hands.append(Hand(cards))
            last = len(self.__hands) - 1
            self.__hands[last].player_hand()

    def uncover_dealer(self):
        self.__hands[0].player_hand()

    # ACTIONS
    def split(self, cards):
        if len(self.__hands) == 1 and self.__hands[0].is_split():

            [new_card1, new_card2] = cards

            last_card = self.__hands[0].pop_card()
            self.__hands[0].push_card(new_card1)
            self.get_hand([last_card, new_card2])
            return True
        else:
            print("[Can't make 'SPLIT' ]")
            return False

    def double_down(self, cards):
        for hand in self.__hands:
            hand.push_card(cards.pop())
            hand.stand()

    def has_split(self):
        return len(self.__hands) == 2

    def show_action(self, turn: bool):
        """ 0 - SUR
            1 - STAND
            2 - HIT
            3 - DD
            4 - SPLIT
        """
        pass

    def declare_bet(self, small_blind):
        print(self.__name, "is now declaring | cash:", self.__cash)
        if self.__cash >= small_blind:
            bet = valid_data.float_input("Declare a bet: ", self.__cash, small_blind)
            self.__cash -= bet
            self.__bet += bet
            return bet
        else:
            return 0.

    def is_active(self):
        for hand in self.__hands:
            if hand.is_active():
                return True
        return False
