from Game import Game

#id will be calculated, if the table is created
#the method to calculate the id is not implemented yet
#so two follwing primenumbers will be multiplied

def getplayer_number_array(array, p_id):
    for i in range(len(array)):
        if array[i].id == p_id:
            return i
    return None


class Table:

    def __init__(self, id, name, link, description, firstplayer):
        self.id = id
        self.name = name
        self.link = link
        self.description = description
        #the players list contains the first player and the other players
        #player is an instance of the place from the database
        self.players = [firstplayer]
        self.play_mode = 5
        self.length = 1
        self.game = None

    def getArrayOfPlayerWithp_id(self, p_id):
        players_inorder = []
        players_inorder = self.players
        nr = getplayer_number_array(self.players, p_id)
        count_of_elements = (nr-(len(self.players)-1-nr))/2
        if count_of_elements < 0:
            for i in range(int(count_of_elements)):
                a=players_inorder[len(players_inorder)-1]
                players_inorder.remove(players_inorder[len(players_inorder)-1])
                players_inorder.insert(0, a)
        else:
            for i in range(int(count_of_elements)):
                a=players_inorder[0]
                players_inorder.remove(players_inorder[0])
                players_inorder.append(a)

        return players_inorder

    def add_player(self, player):
        self.players.append(player)
        self.length += 1

    def check_is_player(self, player):
        for p in self.players:
            if p.id == player.id:
                return True
        return False

    def remove_player(self, player):
        self.players.remove(player)
        self.length -= 1

    def start_game(self):
        player_ids = []
        for p in self.players:
            player_ids.append(p.id)
        self.game = Game(self.play_mode, player_ids)
        self.game.Gamestart(0)


    def add_Bet(self, player_id, player_bet):
        for i in range(len(self.game.players)):
            if self.game.players[i].id  == player_id:
                self.game.players[i] = self.game.add_Bet(self.game.players[i], player_bet)
                break

    def Select_Trumpf(self, player_id, trumpf):
        for i in range(len(self.game.players)):
            if self.game.players[i].id  == player_id:
                self.game.players[i] = self.game.Select_Trumpf(self.game.players[i], trumpf)
                break

    def play_Card(self, player_id, hand_nr):
        for i in range(len(self.game.players)):
            if self.game.players[i].id == player_id:
                self.game.players[i] = self.game.play_Card(hand_nr, self.game.players[i])
                if len(self.game.stack) == 5:
                    self.game.end_of_round()
                self.Is_Game_Over()
                break

    def Is_Game_Over(self):
        if self.game.players[self.game.current_player_nr].hand == []:
            self.end_of_game_screen = True
            return True
        else:
            self.end_of_game_screen = False
            return False

    def Have_you_won(self, player_id):
        for i in range(len(self.game.players)):
            if self.game.players[i].id  == player_id:
                winner = self.game.End_of_Game()
                for w in winner:
                    if w.id == player_id:
                        return True
                    else:
                        return False
                    break

    #give the game state back
    #the game states: 0 = bet, 1 = select trumpf, 2 = play card and 3 = end of the game
    def get_game_state(self, player_id):
        data = []
        for i in range(len(self.game.players)):
            if self.game.players[i].id == player_id:
                #erste Zeile: game state: 0 = bet, 1 = select trumpf, 2 = play card, 3 = end of the game
                if self.game.player_search:
                    data.append(0)
                elif self.game.trumpf_select:
                    data.append(1)
                elif self.end_of_game_screen:
                    data.append(3)
                    #erweiterete Zeile 2: have you won: 0 = false, 1 = true
                    if self.Have_you_won(player_id):
                        data.append(1)
                    else:
                        data.append(0)
                else:
                    data.append(2)
                #zweite Zeile: is player action: 0 = false, 1 = true
                if self.game.players[i].action or (self.game.trumpf_select and self.game.select_player.id == player_id):
                    data.append(1)
                else:
                    data.append(0)
                #dritte Zeile: which cards are in the hand
                cards = []
                for c in self.game.players[i].hand:
                    cards.append(c.id)
                data.append(cards)
                #vierte Zeile: which cards are in the stack (stack: 0: card_id, 1: player_id)
                stack = []
                for s in self.game.stack:
                    stack.append((s[0].id, s[1]))
                data.append(stack)
                #fünfte Zeile: which color is the trumpf and which cord is called
                info = (self.game.trumpf, self.game.lowest_bet)
                data.append(info)
                #sechste Zeile: number of stacks
                data.append(self.game.number_of_stacks)
                #siebte Zeile: last stack
                data.append(self.game.last_stack)

        return data



    def set_playmode(self, new_play_mode):
        self.play_mode = new_play_mode
