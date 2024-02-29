from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("Home.html",  user=current_user)

@views.route('/create-table', methods=['GET', 'POST'])
@login_required
def create_table():
    return render_template("createTabel.html", user=current_user)

@views.route('/join-table', methods=['GET', 'POST'])
@login_required
def join_table():
    return render_template("joinTable.html", user=current_user)



