class Card:
    figures = [str(x) for x in range(2, 11)] + ['J', 'Q', 'K', 'A']
    suits = ("\u2663", "\u2666", "\u2665", "\u2660")

    def __init__(self, num1, num2):
        """
        :param suit: suit in [0,1,2,3]
        :param figure: figure in [0,1,...,12]
        """
        self.__suit = Card.suits[suit]
        self.__figure = Card.figures[figure]
        self.__pts = 0
        self.__is_ace = False
        self.__covered = True
        self.__set_points(figure + 2)

    def __str__(self):
        if not self.__covered:
            return self.__figure + self.__suit
        else:
            return 'XX'

    def __eq__(self, other):
        check = False
        if not other.is_covered and not self.is_covered():
            check = other.get_figure() == self.__figure
        return check

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
    
    def is_covered(self):
        return self.__covered

    def get_figure(self):
        return self.__figure

    def uncover(self):
        self.__covered = False

    def cover(self):
        self.__covered = True
