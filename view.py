from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import os
import app
from app import tables
from Tabel import *

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
        first_player = current_user
        tables.append(Table(len(tables), table_name, f"/table/{len(tables)}", table_description, current_user))
        print(f"Table name: {table_name}, Table description: {table_description}")
        return redirect(url_for('views.table', table_id=len(tables)))

    return render_template("createTabel.html", user=current_user)

@views.route('/join-table', methods=['GET', 'POST'])
@login_required
def join_table():
    print(tables)
    return render_template("joinTable.html", user=current_user, tables=tables)

@views.route('/table/<int:table_id>', methods=['GET', 'POST'])
@login_required
def table(table_id):
    #TODO: Add the user to the table
    return render_template("table.html", user=current_user, table= tables[table_id-1])






