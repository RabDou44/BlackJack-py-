from Player import Player
from Card import Card
from random import randint


def random_card():
    return Card(randint(0, 3), randint(0, 12))


pl1 = Player('Swietopelek', 2300.)
pl2 = Player('Mieszko', 3500.)
dealer = Player('DEALER', 100000.)

print(pl1)
print(pl2)
print(dealer)

dealer.get_hand([Card(0, 12), Card(1, 12)])
pl1.get_hand([Card(0, 11), Card(2, 12)])
dealer.uncover_dealer()

print(pl1)
print(pl2)
print(dealer)
print()

'''


'''
pl2.get_hand([Card(0, 6), Card(1, 6)])

print(pl1)
print(pl2)
print(dealer)
print()

pl2.split([Card(0, 7), Card(2, 9)])

print(pl1)
print(pl2)
print(dealer)
print()

players = [pl1, pl2]

for player in players:
    if player.has_split():
        card_list = [random_card(), random_card()]
        player.double_down(card_list)
    else:
        player.double_down([random_card()])

print(pl1)
print(pl2)
print(dealer)
print()
