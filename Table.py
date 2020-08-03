from random import shuffle
from Player import Player
from Card import Card
import os
import valid_data

bank_balance = 10000.


class Table:
    """
        TAble - provides functionalities enabling the BJ game
        1 - 8 PLAYERS PLAY
        takes
    """
    small_blind = 10.

    @staticmethod
    def higher_basic_stake():
        stake = Table.small_blind

        if stake % 10. == 5. or stake % 10. == 2.5:
            Table.small_blind *= 2
        elif stake == 0.:
            Table.small_blind *= 2.5

    @staticmethod
    def make_deck(num_talias):
        """
        CASINO USE AS MANY TALIAS AS PLAYERS
        => depends on object not class
        :return: list od decks
        """
        deck = []
        for col in range(4):
            for fig in range(2, 15):
                deck += num_talias * [Card(col, fig)]
        shuffle(deck)
        return deck

    def __init__(self):
        num = valid_data.int_input("How many players?")
        self.__how_many_players = num
        self.__players = []
        self.__bank: float = 0

        # first Player DEALER
        self.__players += [Player("DEALER", bank_balance)]

        for index in range(num):
            player_name = valid_data.str_input("Type your name: ", 8)  # character limit
            player_cash = valid_data.float_input("Type the cash you have ($)", 10000., 10.)

            if player_cash > 10.:
                self.__players += [Player(player_name, player_cash)]
            else:
                print("Sorry but you can't join the table")
                num, index = num - 1, index - 1

        self.__deck = Table.make_deck(num)

    def __ask_to_continue(self):
        """
        not used in in the first version
        :return:
        """
        check = False
        for player in self.__players:
            ans = valid_data.yn_input("Do you want to continue playing BJ?")
            if ans == 'y':
                check = True
                break

        return check

    def __GAME_STATE(self):
        clear = lambda: os.system('clear')
        clear()

        """
        prints ALL players

        ##output:
            DEALER CARD: 3 \u2660 (+ other coards)
            -------------------------------------------
            1. DAVE cash $$$$ / $$$$ [cards pts / cards pts]
            2. ANY ...
            3. ...
            ....
            ------------------------------------------
        """
        line, t, size = (30 * "-" + '\n', 1, len(self.__players))

        out_str = "" + str(self.__players[0]) + '\n'
        out_str += line
        for player in self.__players[1:]:
            out_str += str(t) + '. ' + str(player)
            if t < size - 1:
                out_str += '\n'

    def __choose_options(self, pl_index):
        """
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

        SURRENDER -  (possible only at the first turn)
        :return:
        """
        pass

    def __collect_cards(self):
        """
        functionality: brings cards back to deck  + reshuffling deck

        takes no arguments
        edits only Players attributes
        :return:
        """
        for player in self.__players:
            cards = player.__give_out_cards()
            self.__deck += cards

        shuffle(self.__deck)

    def __draw_card(self, how_many_cards):
        size = len(self.__deck)
        return self.__deck[size - how_many_cards - 1:]

    def __deal_cards(self, player_num):
        """
        give cards to each player
        :return:
        """
        for index in range(1, player_num):
            cards = self.__deck.pop()
            cards += self.__deck.pop()
            self.__players[index].accept_cards(cards)

    def __print_final(self):
        for player in self.__players:
            print(player.__str_results)

    def begin_the_game(self):
        """
        After Table was initiated:
            - all players are present (no one new can join)
            - all players have cash > basic_stake

        Scheme of the game
            1) collect bets
            2) deal cards

        :return: None
        """

        bets = []

        # collect bets & dealing cards
        for ply_ix in range(1, len(self.__players)):
            bets += [self.__players[ply_ix].declare_bet(Table.small_blind)]
            cards = [self.__deck.pop(), self.__deck.pop()]
            self.__players[ply_ix].accept_cards(cards)

        self.__GAME_STATE()
        input()

        # deal cards
        for ply_ix in range(len(self.__players)):
            cards = []
            cards += [self.__deck.pop(),self.__deck.pop()]
            self.__players[ply_ix].accept_cards(cards)

        # is there any BLACKJACK
        self.__GAME_STATE()

    """
        # players make actions
        for player in self.__players[1:]:
            if not player.is_playing():
                continue
                
            # OPTIONS : HIT STAND DD INSURANCE
            not_finished = True
            while not_finished: 

            # print GAME STATE

        # DEALER show his cards and recollect untill his has < 17
        dealer_pts = self.__players[0].count_points()
        self.__GAME_STATE()

        while dealer_pts < 17:
            card = self.__deck.pop()
            self.__players[0].accept_card(card)
            dealer_pts = card.count_points()

        # END
        for ply_ix in range(len(self.__players)):
            cards
    """