from app import db
from models import User


class Table:

    def __init__(self, name, link, description, firstplayer):
        self.name = name
        self.link = link
        self.description = description
        #the players list contains the first player and the other players
        #player is an instance of the S_Player class
        self.players = [firstplayer]
        self.game = None

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def start_game(self):
        #TODO: create the game
        pass


class S_Player:

    def __init__(self, id, nickname):
        if db.session.query(User).filter_by(id=id).first() and db.session.query(User).filter_by(nickName=nickname).first():
            self.id = id
            self.nickname = nickname
        else:
            raise ValueError("The user don't exist in the database.")
