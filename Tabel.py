from app import db
from models import User

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
        self.length +=1

    def check_is_player(self, player):
        for p in self.players:
            if p.id == player.id:
                return True
        return False

    def remove_player(self, player):
        self.players.remove(player)
        self.length -=1

    def start_game(self):
        player_ids = []
        for p in self.players:
            player_ids.append(p.id)

        self.game = Game(self.play_mode, player_ids)
        self.start_game()

    def set_playmode(self, new_play_mode):
        self.play_mode = new_play_mode
