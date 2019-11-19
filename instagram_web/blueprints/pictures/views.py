from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User, Pictures
import os
import boto3
import botocore
from app import s3
from flask_login import current_user
import uuid


pictures_blueprint = Blueprint('pictures',
                               __name__,
                               template_folder='templates')


@pictures_blueprint.route('/upload_image', methods=['GET'])
def uploadnew():
    return render_template('pictures/new.html')


@pictures_blueprint.route('/upload_image', methods=['POST'])
def create():
    picture = request.files.get('picture')
    randomString = uuid.uuid4().hex
    randomString = randomString[0:11]
    picture.filename = randomString + '.png'
    try:
        s3.upload_fileobj(
            picture,
            os.environ.get("S3_BUCKET"),
            picture.filename,
            ExtraArgs={
                "ACL": 'public-read',
                "ContentType": picture.content_type
            }
        )
        Pictures(picture=picture.filename, user=current_user.id).save()
    except:
        flash('Upload unsuccessful')

    return redirect(url_for('show', username=current_user.username))
