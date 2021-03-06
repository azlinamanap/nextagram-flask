from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User, Pictures
import os
import boto3
import botocore
from app import s3
from flask_login import current_user
import uuid

posts_blueprint = Blueprint('posts', __name__, template_folder='templates')


@posts_blueprint.route('/<picture>', methods=['GET'])
def pagefor(picture):

    pic = Pictures.get_or_none(Pictures.picture == picture+'.png')
    user = User.get_or_none(User.id == pic.user_id)

    if pic:
        return render_template('posts/post.html', pictures=pic, user=user)
    else:
        return 'No such post available'
