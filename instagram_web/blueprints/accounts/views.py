from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import os

accounts_blueprint = Blueprint('accounts',
                               __name__,
                               template_folder='templates')

# SIGNUP:


@accounts_blueprint.route('/signup', methods=['GET'])
def new():
    return render_template('accounts/new.html')
    # to display some html


@accounts_blueprint.route('/signup', methods=['POST'])
def signup():

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    check_username = User.get_or_none(User.username == username)
    check_email = User.get_or_none(User.email == email)

    if check_email:
        flash('Email already used to sign up. Please use another.', 'danger')
        return render_template('accounts/new.html')

    if check_username:
        flash('Username already taken. Please choose another.', 'danger')
        return render_template('accounts/new.html')

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    if new_user.save():
        login_user(new_user)
        flash('Succesfully signed up for your account. You are now logged in')
        return redirect(url_for('home', username=username))
    else:
        return render_template('accounts/new.html', username=request.form.get('username'), email=request.form.get('email'))

# LOGOUT:


@accounts_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.', 'info')
    return redirect(url_for('home'))

# SIGNIN


@accounts_blueprint.route('/signin', methods=['GET'])
def signin():
    return render_template('accounts/signin.html')


@accounts_blueprint.route('/signin', methods=['POST'])
def signedin():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get_or_none(username=username)
    # password_to_check
    if user:
        # if has user
        check_pass = check_password_hash(user.password, password)
        if check_pass:
            login_user(user)
            flash('Login successful.')
            return redirect(url_for('home'))
        else:
            flash('Invalid password. Please try again.', 'danger')
            return render_template('accounts/signin.html')
    else:
        # if no user found
        flash('No user found. Please check the username.', 'danger')
        return render_template('accounts/signin.html')


@accounts_blueprint.route('/<username>', methods=["GET"])
def show(username):

    pass


@accounts_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@accounts_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@accounts_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
