from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    #unique = True means that the email can only be used once
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    nickName = db.Column(db.String(150), unique = True)
    profile_description = db.Column(db.String(150), default="I am a user of this website!")
    img_profile = db.Column(db.String(150), default = "default.png")

class Moderator_Rights(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grade = db.Column(db.Integer, default = 1)
    user = db.relationship('User')