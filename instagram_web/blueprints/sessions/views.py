from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import random
import string


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')


@sessions_blueprint.route('/signin', methods=['GET'])
def signin():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get_or_none(username=username)
    # password_to_check
    if user:
        # if has user
        check_pass = check_password_hash(user.password, password)
        if check_pass:
            login_user(user)
            # flash success message
            return redirect(url_for('sessions.new'))
        else:
            flash('Invalid password. Please try again.')
            return render_template('sessions/new.html')
    else:
        # if no user found
        flash('No user found')
        return render_template('sessions/new.html')
