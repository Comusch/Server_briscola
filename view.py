from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import os
from models import User
import app
from app import tables
from Tabel import *
from app import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("Home.html",  user=current_user, tables=tables)

@views.route('/changeProfil', methods=['GET', 'POST'])
@login_required
def changeProfil():
    if request.method == 'POST':
        if "image" in request.files:
            print("image")
            image = request.files["image"]
            print("lol")
            image_filename = f"{current_user.id}_profil.png"
            image_path = os.path.join("static", "Profil_images", image_filename)
            print(image_path)
            image.save(image_path)
            current_user.img_profile = image_filename
            print(current_user.img_profile)
            flash("Image saved!", category='success')
    return render_template("addProfile.html", user=current_user)

@views.route('/create-table', methods=['GET', 'POST'])
@login_required
def create_table():
    if request.method == 'POST':
        table_name = request.form.get('name-table')
        table_description = request.form.get('discription')
        first_player = User.query.filter(User.id == current_user.id).first()
        tables.append(Table(len(tables), table_name, f"/table/{len(tables)}", table_description, firstplayer=first_player))
        print(f"Table name: {table_name}, Table description: {table_description}")
        return redirect(url_for('views.table', table_id=(len(tables)-1)))

    return render_template("createTabel.html", user=current_user)

@views.route('/join-table', methods=['GET', 'POST'])
@login_required
def join_table():
    print(tables)
    return render_template("joinTable.html", user=current_user, tables=tables)

@views.route('/table/<int:table_id>', methods=['GET', 'POST'])
@login_required
def table(table_id):
    print(tables[table_id].check_is_player(current_user))
    #show which player is in table
    print("Player in table")
    for p in tables[table_id].players:
        print(p.nickName)
    if tables[table_id].check_is_player(current_user) == False:
        new_player = User.query.filter(User.id == current_user.id).first()
        tables[table_id].add_player(new_player)
        print("Player added!")
        flash("You are now a player of the table!", category='success')

    if tables[table_id].length != tables[table_id].play_mode:
        return render_template("load_side.html", user=current_user, table= tables[table_id])
    else:
        flash("The table is full!", category='success')
        return redirect(url_for('views.join_table'))

@views.route('/table/<int:table_id>/player_data', methods=['GET', 'POST'])
@login_required
def player_data(table_id):

    #add ficktive players to test the game
    #it should be removed later
    if tables[table_id].length != tables[table_id].play_mode:
        tables[table_id].add_player(User.query.filter(User.id == tables[table_id].length).first())
    #end of the test

    #start the game
    if tables[table_id].length == tables[table_id].play_mode:
        tables[table_id].start_game()
        print("Game started!")

    player_data = []
    player_data.append((tables[table_id].length, tables[table_id].play_mode))
    for p in tables[table_id].players:
        player_data.append((p.nickName, p.img_profile))

    return jsonify(player_data)

@views.route('/table/<int:table_id>/game', methods=['GET', 'POST'])
@login_required
def game(table_id):
    return render_template("game.html", user=current_user, table=tables[table_id], players=tables[table_id].getArrayOfPlayerWithp_id(current_user.id))


#TODO: Problems to fix: when the button is clicked, the game should be updated emidiatly (Java Script)
#TODO: The sorting of the playernames are incorrect and the card on the table should match together (Java Script)
#TODO: the fithst card is not shown, because of the instant update (Python)
#TODO: the lable in which stack they are and who wants to play is not shown (Java Script)
@views.route('/table/<int:table_id>/game_data', methods=['GET', 'POST'])
@login_required
def game_data(table_id):
    data =[]
    if len(tables) > table_id:

        if tables[table_id].game.player_search and tables[table_id].game.players[tables[table_id].game.current_player_nr].id != current_user.id:
            i = tables[table_id].game.current_player_nr
            #the play botes skip the bet
            tables[table_id].game.players[i] = tables[table_id].game.add_Bet(tables[table_id].game.players[i], 20)
        elif tables[table_id].game.play_mode and tables[table_id].game.players[tables[table_id].game.current_player_nr].id != current_user.id:
            i = tables[table_id].game.players[tables[table_id].game.current_player_nr].id
            #the bots always play the first card
            tables[table_id].play_Card(i, 0)

        data = tables[table_id].get_game_state(current_user.id)
        print(data)

    else:
        data = None
    return jsonify(data)

#then the webside is finished with a five player mode
@views.route('/table/<int:table_id>/send_action', methods=['GET', 'POST'])
@login_required
def send_action(table_id):
    if request.method == 'POST':
        #action: 1= bet, 2= select trumpf, 3= play card
        data = request.get_json()
        print(data)
        if data['action'] == 1:
            tables[table_id].add_Bet(current_user.id, data['bet'])
        elif data['action'] == 2:
            tables[table_id].Select_Trumpf(current_user.id, data['color'])
        elif data['action'] == 3:
            tables[table_id].play_Card(current_user.id, data['id_Hand'])

    return jsonify("Data received!")









