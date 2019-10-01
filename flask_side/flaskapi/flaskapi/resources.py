# from datetime import datetime

from flask import request

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

from flask_restful import Resource

from flaskapi.flaskapi.models import User as UserModel
from flaskapi.flaskapi.request_parsers import login_parser, user_parser


def _get_current_user():
    cur_user_email = get_jwt_identity()
    user = UserModel.find_by_email(cur_user_email)
    return user


class Home(Resource):
    def get(self):
        return {
            'message':
            'Welcome, to register send a POST request to /user endpoint with \
            your email, password and doc_number, then, make a request to \
            /login to authenticate'
        }


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
        user = _get_current_user()
        if not user:
            return {'message': 'User not found'}, 404
        return {'message': 'Success', 'data': user.to_dict()}, 200

    def post(self):
        data = user_parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {'message': 'This email is already been used'}, 400
        if UserModel.find_by_doc_number(data['doc_number']):
            return {'message': 'This doc_number is already been used'}, 400
        data['password'] = UserModel.generate_hash(data['password'])
        new_user = UserModel(**data)
        new_user.save_to_db()
        return {
            'message': 'User sucessfully registered',
            'data': new_user.to_dict()
        }, 201

    @jwt_required
    def patch(self):
        user = _get_current_user()
        if not user:
            return {'message': 'User not found'}, 404
        if not request.json:
            return {'message': 'You should send a JSON body'}, 400
        user.update_object_on_db(request.json)
        return {
            'message': 'User successfully updated',
            'data': user.to_dict()
        }

    @jwt_required
    def delete(self):
        user = _get_current_user()
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User successfully deleted'}, 204


class Deposit(Resource):
    pass


class Withdraw(Resource):
    pass


class Transfer(Resource):
    pass


class Statements(Resource):
    pass
