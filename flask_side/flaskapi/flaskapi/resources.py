# from datetime import datetime

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

from flask_restful import Resource

from flaskapi.flaskapi.models import User as UserModel
from flaskapi.flaskapi.request_parsers import login_parser


class Home(Resource):
    def get(self):
        return {'Hello': 'World'}


class Login(Resource):
    def post(self):
        data = login_parser.parse_args()
        user = UserModel.find_by_email(data['email'])
        if not user or \
           not UserModel.verify_hash(data['password'], user.password):
            return {
                'message': 'Wrong credentials, please check email and password'
            }, 401
        return {
            'message': 'Successful authenticated',
            'token': create_access_token(identity=user.email)
        }, 200


class User(Resource):
    @jwt_required
    def get(self):
        cur_user_email = get_jwt_identity()
        user = UserModel.find_by_email(cur_user_email)
        return user.to_dict()


class Deposit(Resource):
    pass


class Withdraw(Resource):
    pass


class Transfer(Resource):
    pass


class Statements(Resource):
    pass
