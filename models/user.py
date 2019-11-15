from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from flask import request
from playhouse.hybrid import hybrid_property
import os


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    password = pw.CharField()
    email = pw.CharField(unique=True)
    profile_picture = pw.TextField(null=True)

    @hybrid_property
    def profile_image_path(self):
        if self.profile_picture:
            return f'https://{os.environ.get("S3_BUCKET")}.s3-eu-west-2.amazonaws.com/' + self.profile_picture
        else:
            return f'https://www.searchpng.com/wp-content/uploads/2019/02/Deafult-Profile-Pitcher.png'

    def validate(self):
        if len(self.password) < 8:
            self.errors.append('Password must be at least 8 characters')
        else:
            self.password = generate_password_hash(self.password)


class Pictures(BaseModel):
    user = pw.ForeignKeyField(User, backref='pictures')
    picture = pw.CharField(null=True)

    @hybrid_property
    def post(self):
        if self.picture:
            return f'https://{os.environ.get("S3_BUCKET")}.s3-eu-west-2.amazonaws.com/' + self.picture
        else:
            return 'Success'
