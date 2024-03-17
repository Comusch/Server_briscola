import Card as cd
import Player as ply

class Game:

    def __init__(self, numb_player, player_ids):
        # create deck
        self.deck = cd.Deck()
        self.deck.shuffle()
        # trumph default
        self.trumpf = 99
        # create (numb_player) player
        self.numb_player = numb_player
        self.players = []

        for i in range(0, self.numb_player):
            self.players.append(ply.Player(player_ids[i]))

        # give the players diffrend hands
        if self.numb_player == 5:
            for i in range(0, 8):
                for i in range(0, self.numb_player):
                    self.players[i].get_Card(self.deck.cards[0])
                    self.deck.cards.remove(self.deck.cards[0])
        self.stack = []
        self.current_player_nr = 0
        # varibles for the bet, which player plays
        self.select_player = None
        self.lowest_bet = 999
        self.agree_number = 0
        # Gamemodi
        self.player_search = True
        self.trumpf_select = False
        self.play_mode = False

        #groups in the game
        self.caller_group = []
        self.defender_group = []


    def Gamestart(self, begin_numb_player):
        #initiate a new game
        for player in self.players:
            player.reset()
        self.stack = []
        #create deck
        self.deck = cd.Deck()
        self.deck.shuffle()

        if self.numb_player == 5:
            for i in range(0, 8):
                print(i)
                self.round_get_one_card()
        #set the player active#
        self.current_player_nr = begin_numb_player
        self.players[self.current_player_nr].action = True
        for player in self.players:
            player.would_play = True

        # Gamemodi
        self.player_search = True
        self.trumpf_select = False
        self.play_mode = False

        self.agree_number = 0
        self.lowest_bet = 99

    #player_bet =? 20 --> player skips
    def add_Bet(self, player, player_bet):
        if player.action and self.player_search and player.would_play:
            if player_bet >= 20:
                player.would_play = False
                self.agree_number += 1
                print("Agree!")
            elif player_bet < self.lowest_bet:
                self.lowest_bet = player_bet
                self.select_player = player
                print(f"Player with the id {player.id} would play")

        if self.agree_number == 4:
            self.player_search = False
            self.trumpf_select = True
            print("next step in the game is possible")

        print(f"Now {self.agree_number} agreed for it, active is {self.players[self.current_player_nr].id}")
        player = self.player_set_action(player)
        return player

    def Select_Trumpf(self, player, trumpf):
        print(self.trumpf_select)
        if self.trumpf_select and player == self.select_player:
            self.set_trumpf(trumpf)
            self.play_mode = True
            self.trumpf_select = False

        self.caller_group.append(player)
        player.set_roll(1)
        for p in self.players:
            if p == player:
                continue
            for i in range(len(p.hand)):
                if p.hand[i].value == self.lowest_bet and p.hand[i].color == trumpf:
                    self.caller_group.append(p)
                    p.set_roll(1)
                    break
                elif i == len(p.hand)-1:
                    self.defender_group.append(p)
                    p.set_roll(2)

        return player

    #Method play Card
    def play_Card(self, hand_nr, player):
        if player.action and self.player_search == False:
            self.stack.append((player.hand[hand_nr], player.id))
            player.remove_Card(player.hand[hand_nr])

            player = self.player_set_action(player)
        return player

    def player_set_action(self, player):
        if self.current_player_nr + 1 >= 5:
            self.current_player_nr = 0
        else:
            self.current_player_nr += 1
        player.action = False
        self.players[self.current_player_nr].action = True
        return player

    #Method set trumpf
    def set_trumpf(self, new_trumpf):
        self.trumpf = new_trumpf

    #Methode check stack gewinn
    def check_win_Stack(self):
        if self.stack != []:
            anfangsfarbe = self.stack[0][0].color
            current_highscard = self.stack[0][0]
            current_playerid = self.stack[0][1]
            for step in self.stack:
                if step[0].color == anfangsfarbe:
                    if step[0].value > current_highscard.value:
                        current_highscard = step[0]
                        current_playerid = step[1]
                        anfangsfarbe = step[0].color
                elif step[0].color == self.trumpf:
                    current_highscard = step[0]
                    current_playerid = step[1]
                    anfangsfarbe = step[0].color

            return (current_highscard, current_playerid)

    #Methode End of the round
    def end_of_round(self):
        current_highscard, current_playerid = self.check_win_Stack()
        winner = None
        for i in range(0, len(self.players)):
            if self.players[i].id == current_playerid:
                winner = self.players[i]
                self.current_player_nr = i
        winner.get_stack_in_collection(self.stack)
        self.clear_stack()
        self.players[self.current_player_nr].action = True

    def End_of_Game(self):
        for player in self.players:
            player = self.getScore(player)
        print("score bord:")
        for player in self.players:
            print(f"Player id: {player.id}, score: {player.score}")

        return self.who_wins()


    def who_wins(self):
        winners = []
        caller_score = 0
        defender_score = 0
        for player in self.caller_group:
            caller_score += player.score
        for player in self.defender_group:
            defender_score += player.score
        if caller_score > defender_score:
            winners = self.caller_group
        else:
            winners = self.defender_group
        return winners

    def getScore(self, player):
        for card in player.collection:
            if card.value == 9:
                player.score +=11
            elif card.value == 8:
                player.score +=10
            elif card.value == 7:
                player.score += 4
            elif card.value == 6:
                player.score +=3
            elif card.value == 5:
                player.score +=2
        return player

    def clear_stack(self):
        self.stack = []

    def round_get_one_card(self):
        for i in range (0, self.numb_player):
            self.players[i].get_Card(self.deck.cards[0])
            self.deck.cards.remove(self.deck.cards[0])

    def output_Stack(self):
        print("-----current stack---------")
        for step in self.stack:
            print(f"Card: color:{step[0].color}, value:{step[0].value}; Player_id: {step[1]}")

    def output_players(self, nr):
        print(f"Player id: {self.players[nr].id}")
        print("Player Hand: ")
        for i in range(0,len(self.players[nr].hand)):
            print(f"Card {self.players[nr].hand[i].id}, {self.players[nr].hand[i].color}, {self.players[nr].hand[i].value}")
        print("----------------------")

