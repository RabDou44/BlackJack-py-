import os
import valid_data

from random import shuffle
from Player import Player
from Deck import Deck
clear = lambda: os.system('clear')


class Table:
    """
        TAble - provides functionalities enabling the BJ game
        1 - 8 PLAYERS PLAY
        takes
      player has 4 options:
      HIT - takes card from deck (DEALER serves)
      STAND - takes no more cards
      DOUBLE DOWN - player can et 100% of his initial bet. Later recieves only one card
      INSURANCE - (possible only when DEALER has ACE faceed up ['soft hand'] )
          allows player to bet that DEALER has a BLACKJACK, by placing
          half of your actual bet on INSURANCE zone
          In case if DEALER has BJ technically u loose but your
          assets u placed on INS zone are doubled and comes back to u
          so u're 0
          In case when DEALER has no BJ
      SPLIT - if both cards are the same player can split them into two hands
      """
    small_blind = 10.
    bank_balance = 10000.

    @staticmethod
    def stake_up():
        stake = Table.small_blind
        if stake % 10. == 5. or stake % 10. == 2.5:
            Table.small_blind *= 2
        elif stake == 0.:
            Table.small_blind *= 2.5

    def __init__(self):

        num = valid_data.int_input("How many players?")

        self.__players = []
        self.__num_players = min(num, 8)
        self.__cards_dealt = False
        self.__bets_declared = False
        self.__dealer_pts = 0
        print()

        for index in range(self.__num_players):
            player_name = valid_data.str_input("Type your name: ", 15)  # character limit
            print(player_name)
            player_cash = valid_data.float_input("Type the cash you have ($)", 10000.)
            print(player_cash)

            if player_cash > 10.:
                self.__players += [Player(player_name, player_cash)]
            else:
                print("Sorry but you can't join the table", player_name)
                index -= 1

        # first Player DEALER
        self.__players = [Player("DEALER", 10000.)] + self.__players

        # assign Deck
        self.__talia = Deck(num)

    def __str__(self):
        clear()
        """
          ##output:
              DEALER CARD: 3 \u2660 (+ other cards)
              -------------------------------------------
              1. DAVE cash $$$$ / $$$$ [cards pts / cards pts]
              2. ANY ...
              3. ...
              ....
              ------------------------------------------
          """
        line, t, size = (100 * "-" + '\n', 1, len(self.__players))
        out_str = "" + str(self.__players[0]) + 10*' '
        out_str += "basic stake: " + str(Table.small_blind) + ' $' + '\n'
        out_str += line

        for player in self.__players[1:]:
            out_str += str(t) + '. ' + str(player)
            if t < size - 1:
                out_str += '\n'
            t += 1

        out_str += '\n' + line
        return out_str

    def deal_cards(self):
        if not self.__cards_dealt:
            for player in self.__players:
                cards = self.__talia.draw_card(2)
                player.get_hand(cards)
            self.__cards_dealt = True
        else:
            print("[Cards are already dealt]")

    def bets_declaration(self):
        for index in range(1, len(self.__players)):
            print(self)
            self.__players[index].declare_bet(Table.small_blind)
        self.__bets_declared = True

    def run_game(self):
        if self.__bets_declared and self.__cards_dealt:
            for player in self.__players:
                print(self)
                if player != self.__players[0]:
                    player.make_action(self.__talia)

    def end_game(self):
        # show the winners and losers
        pts = self.__players[0].uncover_dealer(self.__talia)
        for player in self.__players:
            player.payoff(pts)
        print(self)
        input()
        for player in self.__players:
            player.collect_cards(self.__talia)




