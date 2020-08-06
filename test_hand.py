from Hand import Hand
from Card import Card
from random import randint

h1 = Hand([Card(2, 3), Card(0, 12)])
h2 = Hand([Card(1, 10), Card(3, 11)])

h1.player_hand()
h2.dealer_hand()

print(h1)
print(h2)

# =os
h1.push_card(Card(0, 3))
print(h1)
h1.pop_card()
h1.pop_card()
h1.pop_card()
h1.push_card(Card(randint(0, 3), randint(0, 12)))
h1.push_card(Card(randint(0, 3), randint(0, 12)))
h1.push_card(Card(randint(0, 3), randint(0, 12)))
h1.push_card(Card(randint(0, 3), randint(0, 12)))
h1.push_card(Card(randint(0, 3), randint(0, 12)))
print(len(h1))


