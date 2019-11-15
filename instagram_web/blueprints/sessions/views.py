from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import random
import string


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')
