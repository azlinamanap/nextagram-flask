from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')
    # to display some html


@users_blueprint.route('/', methods=['POST'])
def create():
    pass
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    if new_user.save():
        return redirect(url_for('home', username=new_user.username))
    else:
        return render_template('users/new.html', username=request.form.get('username'), email=request.form.get('email'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):

    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
