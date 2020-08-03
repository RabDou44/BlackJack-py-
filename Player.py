from Card import Card
from typing import List
import valid_data

Hand = List[Card]
Deck = List[Hand]


class Player:
    options = ['SURRENDER', 'STAND', 'HIT', 'DOUBLE DOWN', 'SPLIT']

    def __init__(self, *args):
        name, cash = args

        self.__name = name
        self.__hands = [[], []]  # 2 hands for cards
        self.__pts = [0, 0]

        self.__cash = cash
        self.__debt = 0
        self.__act_bet = 0

        self.__aces = 0
        self.__split = False
        self.__DD = False
        self.__plays = name != 'DEALER'

    def __str__(self):
        """
        :return: string containing each player state
        """
        out_str = "%-8s " % self.__name

        if self.__name != "DEALER":
            out_str += " cash/bet:   %5.2f /   %5.2f $" % (self.__cash, self.__act_bet)
            out_str += "["

            # first hand
            for card in self.__hands[0]:
                out_str += ' ' + str(card)
            out_str += " %5s pts" % self.__pts_str(0)

            # second hand
            if self.__split:
                out_str += '|'
                for card in self.__hands[1]:
                    out_str += str(card) + ' '
                out_str += " %4s pts" % self.__pts_str(1)
            out_str += "]"
        else:
            out_str += str(self.__hands[0][0]) + ' XX'

        return out_str

    def __count_points(self):
        """
        used when the cards are dealt
        :return:
        """
        points = []
        h = 1 if self.__split else 0

        for index in range(1 + h):
            part_sum = 0
            for card in self.__hands[index]:

                car_pts = card.points()
                if car_pts == 11:
                    self.__aces += 1
                part_sum += car_pts

            points += [part_sum]

        [self.__pts[0], self.__pts[1]] = [points[0], points[1] if len(points) > 1 else 0]

    def __double_bet(self):
        self.__cash -= self.__act_bet
        self.__act_bet *= 2

    def __give_out_cards(self):

        cards = self.__hands[0]
        if self.__split:
            cards += self.__hands[1]

        self.__hands = [[], []]
        self.__pts = [0, 0]
        self.__act_bet = 0
        self.__aces = 0
        self.__plays = False
        self.__DD = False
        self.__split = False

        return cards

    def __dealer_bust(self):

        if self.__split:
            if self.__pts[1] <= 21:
                half = self.__act_bet / 2
                self.__act_bet /= 2
                self.__cash += half * 2

        if self.__pts[0] <= 21:
            self.__cash += self.__act_bet * 2

        return self.__give_out_cards()

    def __pts_str(self, which_hand):

        self.__count_points()
        pt_str = ""
        hand_pts = self.__pts[which_hand]
        aces = self.__aces

        if hand_pts > 11 or aces == 0:
            pt_str += str(hand_pts)
        elif self.__aces > 0:
            pt_str += "%2d/%2d" % (hand_pts, hand_pts + 10)

        return pt_str

    def __no_bj(self):
        if self.__split:
            return self.__pts[0] < 21 and self.__pts[1] < 21
        return self.__pts[0] < 21

    def is_playing(self):
        return self.__plays

    def join_game(self):
        self.__plays = True

    def accept_cards(self, cards):
        if not self.__plays:
            self.__plays = True
        self.__hands[0] += cards
        self.__count_points()

        if not self.__no_bj():
            self.__plays = False

    def declare_bet(self, small_blind):
        print(self.__name, "is now declaring | cash:", self.__cash)
        if self.__cash >= small_blind:
            bet = valid_data.float_input("Declare a bet: ", self.__cash, small_blind)
            self.__cash -= bet
            self.__act_bet += bet
            return bet
        else:
            return 0.

    def is_busted(self):
        if self.__split:
            if self.__pts[0] > 21 and self.__pts[1] > 21:
                return True
            return False
        elif self.__pts[0] > 21:
            return True
        return False

    def is_split(self):
        if not self.__split:
            hand = self.__hands[0]
            return hand[0] == hand[1]
        return False

    def split(self, cards):
        """
        options
        """

        [card1, card2] = cards

        self.__hands[1] = []
        self.__split = True

        self.__hands[1] += self.__hands[0][1:] + [card2]
        self.__hands[0] = self.__hands[0][:1] + [card1]

        self.__double_bet()
        return self.is_busted()

    def surrender(self):
        self.__cash += self.__act_bet
        return self.__give_out_cards()

    def hit(self, card):
        if self.__split:
            if len(self.__hands[0]) > len(self.__hands[1]) and self.__pts[1] < 21:
                self.__hands[1] += [card]
            else:
                self.__hands[0] += [card]

        else:
            self.__hands[0] += [card]

        return self.is_busted()

    def is_DD(self):
        is_possible = True
        for hand in self.__hands:
            if len(hand) > 2:
                is_possible = False
        return is_possible

    def double_down(self, cards: List[Card]):
        """
        double down might be called in two options
        after split or after dealing cards
        :param cards:
        :return:
        """
        if not self.__DD:
            self.__plays = False
            self.__double_bet()
            self.__DD = True

            self.__hands[0] += [cards.pop()]

            if self.__split:
                self.__hands[1] += [cards.pop()]

        return True

    def show_options(self, turn: bool):
        print(self.__name, '\'s turn')
        t = 0
        for opt in Player.options:
            if opt == 'SURRENDER' and not turn:
                continue
            if opt == 'DOUBLE DOWN' and not self.is_DD():
                continue
            if opt == 'SPLIT' and not self.is_split():
                continue

            print(str(t) + '.', opt)
            t += 1

    def finalize_game(self, dealer_pts: float):
        """
        checks out all players finally
        :param dealer_pts:
        :return:
        """
        if dealer_pts > 21:
            return self.__dealer_bust()

        if self.__split:
            if self.__pts[1] > dealer_pts:
                half = self.__act_bet / 2
                self.__act_bet /= 2
                self.__cash += half * 2

        if self.__pts[0] > dealer_pts:
            self.__cash += self.__act_bet * 2

        return self.__give_out_cards()

    def str_res(self, dealer_pts, hand):
        return 'WIN' if self.__pts[hand] == 21 or self.__pts[hand] > dealer_pts else 'LOST'

    def str_results(self, dealer_pts=20):

        out_str = '' + self.__name + " "

        if self.is_busted():
            out_str += "[%6s]" % 'BUSTED'
        else:
            out_str += "[%4s" % self.str_res(dealer_pts, 0)
            if self.__split:
                out_str += "/%4s" % self.str_res(dealer_pts, 1)
            out_str += "]"
        return out_str

    def dealer_collect(self):
        if self.__name == 'DEALER':
            return self.__pts[0] < 17
        else:
            return False

    def dl_pts(self):
        return self.__pts[0]
