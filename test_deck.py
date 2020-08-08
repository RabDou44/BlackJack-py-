from Deck import Deck

d1 = Deck()
d2 = Deck(0)

print(len(d1), '\n', str(d1))
print(len(d2), '\n', str(d2))

for c in range(21):
    card = d1.draw_card()
    print(card)
    d2.push_cards(card)
    print("TEST_PASSED" if len(d1) + len(d2) == 52 else "TEST FAILED")
    print(len(d1), len(d2))
    print(d2)
