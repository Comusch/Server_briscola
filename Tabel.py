from app import db
from models import User

#id will be calculated, if the table is created
#the method to calculate the id is not implemented yet
#so two follwing primenumbers will be multiplied

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

    def add_player(self, player):
        self.players.append(player)
        self.length +=1

    def remove_player(self, player):
        self.players.remove(player)
        self.length -=1

    def start_game(self):
        #TODO: create the game
        pass

    def set_playmode(self, new_play_mode):
        self.play_mode = new_play_mode


class S_Player:

    def __init__(self, id, nickname):
        if db.session.query(User).filter_by(id=id).first() and db.session.query(User).filter_by(nickName=nickname).first():
            self.id = id
            self.nickname = nickname
        else:
            raise ValueError("The user don't exist in the database.")
