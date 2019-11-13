from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, Pictures
from instagram_web.blueprints.accounts.views import accounts_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(accounts_blueprint, url_prefix="/accounts")

# app.register_blueprint(sessions_blueprint, url_prefix="/sessions")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/<username>', methods=['GET'])
def show(username):
    pictures = Pictures.select()
    user = User.get_or_none(User.username == username)
    if user:
        return render_template('accounts/profile.html', user=user, pictures=pictures)
    else:
        flash('User not found.')
        return render_template('accounts/search_error.html')
