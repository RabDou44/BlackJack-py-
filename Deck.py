from Card import Card
from random import shuffle


class Deck:

    def __init__(self, num=1):
        self.__container = []
        for col in range(4):
            for fig in range(13):
                self.__container += num * [Card(col, fig)]
        shuffle(self.__container)
        self.__size = 52*num

    def draw_card(self, how_many_cards=1) -> list:
        hand = []
        new_size = self.__size - how_many_cards

        if new_size > 0:
            self.__size = new_size
            hand = self.__container[new_size:]
            self.__container = self.__container[:new_size]
        else:
            self.__size = 0
            hand = self.__container
            self.__container = []

        return hand

    def __len__(self):
        return self.__size

    def push_cards(self, cards):
        if isinstance(cards, Card):
            self.__container += [cards]
            self.__size += 1
        elif isinstance(cards, list):
            self.__container += cards
            self.__size += len(cards)

    def __str__(self):
        output = ''
        for card in self.__container:
            output += ' '+str(card)
        return output
