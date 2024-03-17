import math
import random

class Card:

    #id is element of [0, 40)
    #
    def __init__(self, id, color, value):
        self.id = id
        self.color = color
        self.value = value

class Deck:

    def __init__(self):
        self.cards = []
        #color: between 0-3, 0: Knüppel, 1: Münze, 2: Kelch, 3: Schwert
        #id: between 0-39
        #value: 0-> 2, 9-> Ass
        for i in range(0, 40):
            c = Card(i, int(i/10), i%10)
            self.cards.append(c)

    def output_deck(self):
        for c in self.cards:
            print(f"Card: {c.id}, {c.color}, {c.value}")

    def shuffle(self):
        deck = self.cards
        deck_new = []
        for i in range(len(self.cards)):
            nr = random.randint(0, len(deck)-1)
            deck_new.append(deck[nr])
            deck.remove(deck[nr])

        self.cards = deck_new













