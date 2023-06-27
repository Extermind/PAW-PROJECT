from . import auth
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from ..database import db
from ..jwt import jwt, roles_required
from ..models import User, Role, Project
import bcrypt


@jwt.user_identity_loader
def user_identity_callback(user):
    return user


@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    if hasattr(user, 'roles'):
        return {'roles': user.roles}
    return {}



@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']

    checkUserUsername = User.query.filter_by(username=username).first()

    checkUserEmail = User.query.filter_by(email=email).first()
    if checkUserUsername or checkUserEmail:
        return jsonify(message='User already exists'), 400

    password = bcrypt.hashpw(data['password'].encode("UTF-8"), bcrypt.gensalt())
    role = Role.get_user_role()

    if not role:
        return jsonify(message='Invalid role'), 400

    user = User(username, email, password)
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()

    return jsonify(message='User registered successfully'), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username and not email:
        return jsonify(message='Username or email is missing'), 400

    if bool(username) == bool(email):
        return jsonify(message='Provide either username or email (not both)'), 400

    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    elif username:
        user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode("UTF-8"), user.password.encode("UTF-8")):  # user.password == password:
        roles = []
        for role in user.roles:
            roles.append({'id': role.id, 'name': role.name})
        access_token = create_access_token(identity=user.id, additional_claims={'roles': roles})
        return jsonify(access_token=access_token), 200

    return jsonify(message='Invalid credentials'), 401





