from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import os

app = Flask(__name__, template_folder='templates')

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/signup', methods=['GET'])
def new():
    return render_template('users/new.html')
    # to display some html


@users_blueprint.route('/', methods=['POST'])
def create():

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    check_username = User.get_or_none(User.username == username)
    check_email = User.get_or_none(User.email == email)

    if check_email:
        flash('Email already used to sign up. Please use another.')
        return render_template('users/new.html')

    if check_username:
        flash('Username already taken. Please choose another.')
        return render_template('users/new.html')

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    if new_user.save():
        login_user(new_user)
        return redirect(url_for('home', username=username))
    else:
        return render_template('users/new.html', username=request.form.get('username'), email=request.form.get('email'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):

    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
