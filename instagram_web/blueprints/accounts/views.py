from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User, Pictures
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import os
import boto3
import botocore
from app import s3

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
        flash('Successfully signed up for your account. You are now logged in')
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return 'NOT VALID'
    else:
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

# to make sure accounts isnt available


@accounts_blueprint.route('/', methods=["GET"])
def index():
    return "PAGE NOT AVAILABLE."

# EDIT PROFILE


@accounts_blueprint.route('/edit', methods=['GET'])
@login_required
def edit():
    return render_template('accounts/edit.html')


@accounts_blueprint.route('/edit', methods=['POST'])
@login_required
def update():
    username = request.form.get('username')
    email = request.form.get('username')
    password = request.form.get('password')
    password = generate_password_hash(password)

    check_username = User.get_or_none(User.username == username)
    check_email = User.get_or_none(User.email == email)

    if check_username:
        flash('Username has already been taken. Please choose another')
        return redirect(url_for('accounts.edit'))

    if check_email:
        flash('Email has already been used. Please use another')
        return redirect(url_for('accounts.edit'))

    if not username:
        username = current_user.username
    if not email:
        email = current_user.email
    if not password:
        password = current_user.password

    User.update(username=username, email=email, password=password).where(
        User.id == current_user.id
    ).execute()

    return redirect(url_for('show', username=username))

# EDIT PROFILE PIC


@accounts_blueprint.route('/edit/upload', methods=['POST'])
@login_required
def uploaded():
    user_file = request.files.get('user_file')
    try:
        s3.upload_fileobj(
            user_file,
            os.environ.get("S3_BUCKET"),
            user_file.filename,
            ExtraArgs={
                "ACL": 'public-read',
                "ContentType": user_file.content_type
            }
        )

        User.update(profile_picture=user_file.filename).where(
            User.id == current_user.id).execute()
    except:
        flash('Profile picture upload unsuccessful.')

    return redirect(url_for('accounts.edit'))
