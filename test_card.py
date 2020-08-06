from Card import Card
from random import randint

for c in range(0, 100):

    col1, col2 = randint(0, 3), randint(0, 3)
    fig1, fig2 = randint(0, 12), randint(0, 12)

    # __str__ and __len__ covered
    card1 = Card(col1, fig1)
    test = 'XX' in str(card1)
    if test:
        test = 0 == len(card1)

    # uncover()
    card1.uncover()
    st_card = "" + Card.figures[fig1] + Card.suits[col1]
    if test:
        test = st_card == str(card1)

    if test:
        print(card1)

    # __pts__
    pts1 = fig1 + 2
    if 10 < pts1 <= 13:
        pts1 = 10
    elif pts1 == 14:
        pts1 = 11

    if test:
        test = len(card1) == pts1

    # ace
    if test:
        if len(card1) == 11:
            test = card1.is_ace()

    # covered
    if test:
        card1.cover()
        test = "XX" == str(card1)

    if test:
        card_copy = Card(col1, fig1)
        print(card1 == card_copy)
        card_copy.uncover()
        print(card1 == card_copy)
        card1.uncover()
        print(card1, card_copy)
        print(card1 == card_copy)

    print("TEST", c, 'PASSED' if test else 'FAILED')

