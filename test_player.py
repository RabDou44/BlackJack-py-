from Player import Player
from Deck import Deck


def print_players(players):
    for player in players:
        print(player)


pl1 = Player('Swietopelek', 2300.)
pl2 = Player('Mieszko', 3500.)
dealer = Player('DEALER', 100000.)

deck_test = Deck()
players = [dealer, pl1,  pl2]

dealer.get_hand(deck_test.draw_card(2))
pl1.get_hand(deck_test.draw_card(2))
pl2.get_hand(deck_test.draw_card(2))
dealer.uncover_dealer()

# print players
print_players(players)

# if split: make split
for player in players:
    if player != dealer and player.has_split():
        player.split(deck_test)

# double_down
for player in players:
    if player != dealer:
        player.double_down(deck_test)

print_players(players)
