
class Player:

    def __init__(self, id):
        self.id = id
        self.action = False
        self.score = 0
        self.would_play = True
        self.hand = []
        self.collection = []
        #roll: caller = 1, defender = 2, none = 0
        self.roll = 0

    def set_roll(self, roll):
        self.roll = roll

    def reset(self):
        self.action = False
        self.score = 0
        self.roll = 0
        self.would_play = True
        self.hand = []
        self.collection = []

    def get_Card(self, c):
        self.hand.append(c)

    def remove_Card(self, c):
        self.hand.remove(c)

    def get_stack_in_collection(self, stack):
        for card in stack:
            self.collection.append(card[0])



