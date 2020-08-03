from random import shuffle
from Player import Player
from Card import Card
import os, sys, valid_data

bank_balance = 10000.
clear = lambda: os.system('clear')


class Table:
    """
        Table - provides functionalities enabling the BJ game
        1 - 8 PLAYERS PLAY
    """
    options = ['SURRENDER', 'STAND', 'HIT', 'DOUBLE DOWN', 'SPLIT']
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

        # check file first
        fname = open(sys.argv[1])
        fline = iter(fname)

        num = int(next(fline))
        self.__how_many_players = num
        self.__players = []
        self.__bank: float = 1000000.

        # first Player DEALER
        self.__players += [Player("DEALER", bank_balance)]

        for index in range(num):
            player_name = next(fline)
            player_name = player_name[:len(player_name) - 1]
            player_cash = float(next(fline))

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
        line, t, size = (60 * "-" + '\n', 1, len(self.__players))

        out_str = "" + str(self.__players[0]) + '\n'
        out_str += line
        for player in self.__players[1:]:
            out_str += str(t) + '. ' + str(player)
            t += 1
            out_str += '\n'

        out_str += line
        print(out_str)

    @staticmethod
    def __choose_options(player, turn):
        """
        player has 4 options:
        HIT - takes card from deck (DEALER serves)
        STAND - takes no more cards
        DOUBLE DOWN - player can et 100% of his initial bet. Later recieves only one card
        INSURANCE - (possible only when DEALER has ACE faceed up ['soft hand'] )
            allows player to bet that DEALER has a BLACKJACK, by placing
            half of your actual bet on INSURANCE zone
            In case if DEALER has BJ technically u loose but your
            assets u placed on INS zone are doubled    and comes back to u
        SPLIT - if both cards are the same player can split them into two hands
        SURRENDER -  (possible only at the first turn)
        :return:
        """
        print()
        for t in range(len(Table.options)):
            if t == 0 and not turn:
                continue
            if t == 3 and not player.is_DD():
                continue
            if t == 4 and not player.is_split():
                continue

            print(str(t) + '.', Table.options[t])

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

    def __draw_card(self, how_many_cards=1):
        size = len(self.__deck)
        hand = self.__deck[size - how_many_cards:]
        self.__deck = self.__deck[:size - how_many_cards]
        return hand

    def __put_cards(self, cards):
        self.__deck += cards

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

    def __ending(self):
        pass

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
        # collect bets & dealing cards
        for ply_ix in range(len(self.__players)):
            if ply_ix > 0:
                self.__players[ply_ix].declare_bet(Table.small_blind)
            cards = self.__draw_card(2)
            self.__players[ply_ix].accept_cards(cards)

        # is there any BLACKJACK
        self.__GAME_STATE()

        # GAME
        for player in self.__players[1:]:
            if not player.is_playing():
                continue

            first_turn = True
            # OPTIONS : 'HIT' 'STAND' 'DD' 'INSURANCE'
            finished = False
            while not finished:
                """
                    showing options - Player
                    making decision - Table
                """
                player.show_options(first_turn)
                first_turn = False if first_turn else first_turn
                choice = valid_data.int_input("Choose option from 0 to 4: ", 4)

                if choice == 0 or choice == 1:
                    """SUR oor STAND"""
                    if choice == 0:
                        cards = player.surrender()
                        self.__put_cards(cards)
                    finished = True

                elif choice == 2:
                    """HIT"""
                    card = self.__draw_card()
                    finished = player.hit(card)

                elif choice == 3:
                    """DD"""
                    card = self.__draw_card()
                    if player.is_split():
                        card += self.__draw_card()
                    finished = player.double_down(card)

                elif choice == 4:
                    """SPLIT"""
                    cards = self.__draw_card(2)
                    finished = player.split(cards)
                else:
                    finished = True
                self.__GAME_STATE()

        # DEALER show his cards and recollect until his has < 17

        while self.__players[0].dealler_collect():
            card = self.__draw_card()
            self.__players[0].accept_card(card)
        # self.__ending()
