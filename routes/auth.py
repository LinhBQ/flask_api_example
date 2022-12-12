from flask import Blueprint, request

BP = Blueprint('auth', __name__)
from common.auth import check_dupplicate_email
from initial.init_database import db
from models.user import User
from schemas.auth import auth_schema
from services.auth import login_required
from services.jwt_token import JWT_Token


@BP.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = auth_schema.load(data)
    if check_dupplicate_email(schema['email']):
        return 'Email already exist'
    user = User(**schema)
    db.session.add(user)
    db.session.commit()
    return schema


@BP.route('/login', methods=['POST'])
def login():
    data =  request.get_json()
    schema = auth_schema.load(data)
    email = schema['email']
    user = User.query.filter_by(email=email).first()

    if user is None:
        return 'This user is not exit'
    
    if user.password != schema['password']:
        return 'Wrong password'
    
    token = JWT_Token()
    return token.generate_token(user)


@BP.route('/info', methods=['GET'])
@login_required
def get_user():
    return {'result': 'ok'}