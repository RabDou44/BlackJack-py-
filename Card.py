class Card:
    figures = [str(x) for x in range(2, 11)] + ['J', 'Q', 'K', 'A']
    suits = ("\u2663", "\u2666", "\u2665", "\u2660", "?")

    def __init__(self, num1, num2):
        self.__suit = Card.suits[num1]
        self.__figure = Card.figures[num2]
        self.__pts = 0
        self.__is_ace = False
        self.__covered = False

        self.__set_points(num2+2)

    def __str__(self):
        if not self.__covered:
            return self.__figure + self.__suit
        else:
            return 'XX'

    def __eq__(self, other):
        return self.__figure == other.get_figure()

    def __len__(self):
        return self.__pts if not self.__covered else 0

    def __set_points(self, num):
        if num <= 10:
            self.__pts = num
        elif num <= 13:
            self.__pts = 10
        else:
            self.__pts = 11
            self.__is_ace = True

    def is_ace(self):
        return self.__is_ace

    def get_figure(self):
        return self.__figure

    def uncover(self):
        self.__covered = False

    def cover(self):
        self.__covered = True
