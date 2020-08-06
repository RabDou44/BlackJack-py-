from Card import Card
from typing import List


class Hand:

    def __init__(self, cards):

        if isinstance(cards, List):
            self.__cards: List[Card] = cards
        elif isinstance(cards, Card):
            self.__cards = [cards]
        else:
            raise TypeError(" 'Cards' is not type List nor Card")

        self.__aces = 0
        self.__pts = 0
        self.__busted = False

    def __len__(self):
        return self.__pts

    def __str__(self):
        """ 32-length string"""
        out_str = ''
        if not self.is_busted():
            local_str = ''
            for card in self.__cards:
                local_str += str(card) + ' '

            out_str += "%-18s" % local_str
            if self.__aces > 0 and self.__pts <= 21:
                out_str += "%2d/%2d" % (self.__pts - 10, self.__pts)
            else:
                out_str += "%5d" % self.__pts

            out_str += ' pts'
        else:
            out_str += '[BUSTED]'
        return out_str

    def __count_pts(self):
        self.__pts = 0
        self.__aces = 0
        card: Card
        for card in self.__cards:

            card_pts = len(card)
            if card_pts == 11:
                self.__aces += 1

            self.__pts += card_pts

    def pop_card(self):
        card = self.__cards.pop()
        self.__count_pts()
        if card.is_ace():
            self.__aces -= 0
        return card

    def push_card(self, card):
        card.uncover()
        self.__cards.append(card)
        self.__count_pts()

    def player_hand(self):
        for card in self.__cards:
            card.uncover()
        self.__count_pts()

    def dealer_hand(self):
        self.__cards[0].uncover()
        self.__cards[1].cover()
        self.__count_pts()

    def is_busted(self):
        return self.__pts > 21
