from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"

tables = []
infinite_counter = 1

def infinite_couterchange(new_value):
    infinite_counter = new_value

def create_app():
    #create the app and the database
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Winnetou"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from view import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    create_database(app)

    # the website is now running
    # in the following the tables and the game mode will be created
    # TODO: create the tables and the game mode


    return app


def create_database(app):
    db_path = os.path.join(os.getcwd(), DB_NAME)
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("Created Database!")

if __name__ == '__main__':
    app = create_app()
    app.run(host='192.168.2.33', use_reloader=False)



