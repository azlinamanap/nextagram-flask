import os
import config
from uuid import uuid4
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from models.base_model import db
from models.user import User
from werkzeug.utils import secure_filename
import boto3
import botocore

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("S3_KEY"),
    aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash('Please log in.')
    return redirect(url_for('accounts.signin'))


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
