from typing import Dict


class Card:
    high_figures: Dict[int, str] = {11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '?'}
    colours = ("\u2663", "\u2666", "\u2665", "\u2660", "?")

    def __init__(self, colour, figure):
        """
        :param colour: int , translated to proper UTF
        :param figure: int
        """
        self.__colour = colour
        self.__figure = figure
        self.__pts = 0
        self.points()

    def __str__(self):
        figure_str = str(Card.high_figures[self.__figure] if self.__figure > 10 else self.__figure)
        return figure_str + Card.colours[self.__colour]

    @property
    def power(self):
        return self.__figure

    def __lt__(self, other):
        return self.__figure < other.power

    def __eq__(self, other):
        return self.__figure == other.power

    def __gt__(self, other):
        return self.__figure > other.power

    def points(self):
        if self.__pts == 0:
            tmp_pts = 0
            fig = self.__figure
            if fig <= 10:
                tmp_pts = fig
            elif fig < 14:
                tmp_pts = 10
            elif fig == 14:
                tmp_pts = 11
            self.__pts = tmp_pts
        return self.__pts
