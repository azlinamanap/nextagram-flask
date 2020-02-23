from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, jsonify
from models.user import User, Pictures
from models.follows import Follows
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import os

follows_blueprint = Blueprint('follows', __name__, template_folder='templates')


@follows_blueprint.route('/<username>', methods=["GET"])
@login_required
def follow(username):
    # Get the user that the current_user wants to follow
    idol = User.get_or_none(User.username == username)

    # If the user does not exist
    if not idol:
        flash("This user does not exist")
        return redirect(url_for('home'))

    # Check that the current_user is not already following the user
    check_follow = Follows.get_or_none(
        (Follows.idol_id == idol.id) & (Follows.fan_id == current_user.id))

    if check_follow:
        flash('You are already following this user.')
        return redirect(url_for('show', username=idol.username))

    # Follow the user
    new_follow = Follows(
        idol=idol.id, fan=current_user.id, is_approved=True)

    new_follow.save()

    if new_follow.save():
        return redirect(url_for('show', username=idol.username))
