# from datetime import datetime

import numbers

from flask import request

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

from flask_restful import Resource

from flaskapi.flaskapi.models import (
    User as UserModel, Transaction as TransactionModel
)
from flaskapi.flaskapi.request_parsers import (
    login_parser, user_parser, self_transaction_parser, transfer_parser
)

DOCUMENTATION = 'github.com/tyronedamasceno/flask-vs-django-api/blob/master/docs.md'


def _create_transaction(user, value):
    t = TransactionModel(user_id=user.id, value=value)
    t.save_to_db()
    return t


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
            /login to authenticate',
            'docs': f'You cand find API documentation at: {DOCUMENTATION}'
        }, 200


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
    @jwt_required
    def post(self):
        data = self_transaction_parser.parse_args()
        value = data['value']
        user = _get_current_user()
        if not user:
            return {'message': 'User not found'}, 404
        if not isinstance(value, numbers.Real):
            try:
                value = float(value)
            except ValueError:
                return {'message': 'Invalid value'}, 400
        if value <= 0:
            return {'message': 'You must deposit a value greater than 0'}, 400
        user.update_balance(value)
        transaction = _create_transaction(user, value)
        return {
            'message': 'Deposit success',
            'data': transaction.to_dict()
        }


class Withdraw(Resource):
    @jwt_required
    def post(self):
        data = self_transaction_parser.parse_args()
        value = data['value']
        user = _get_current_user()
        if not user:
            return {'message': 'User not found'}, 404
        if not isinstance(value, numbers.Real):
            try:
                value = float(value)
            except ValueError:
                return {'message': 'Invalid value'}, 400
        if value <= 0:
            return {'message': 'You must withdraw a value greater than 0'}, 400
        if value > user.balance:
            return {'message': 'You have not enough balance'}, 400
        user.update_balance(-value)
        transaction = _create_transaction(user, -value)
        return {
            'message': 'Withdraw success',
            'data': transaction.to_dict()
        }


class Transfer(Resource):
    @jwt_required
    def post(self):
        data = transfer_parser.parse_args()
        value = data['value']
        user = _get_current_user()
        if not user:
            return {'message': 'User not found'}, 404
        if not isinstance(value, numbers.Real):
            try:
                value = float(value)
            except ValueError:
                return {'message': 'Invalid value'}, 400
        if value <= 0:
            return {'message': 'You must transfer a value greater than 0'}, 400
        if value > user.balance:
            return {'message': 'You have not enough balance'}, 400

        destiny_user = UserModel.find_by_doc_number(data['destiny_doc_number'])
        if not destiny_user:
            return {'message': 'Destiny User not found'}, 404
        if destiny_user.id == user.id:
            return {'message': 'You cant transfer to yourself'}, 400
        user.update_balance(-value)
        destiny_user.update_balance(value)
        transaction = _create_transaction(user, -value)
        destiny_transaction = _create_transaction(destiny_user, value)

        return {
            'message': 'Success transfer',
            'data': transaction.to_dict(),
            'data_destiny': destiny_transaction.to_dict()
        }, 200


class Statements(Resource):
    @jwt_required
    def get(self):
        user = _get_current_user()
        if not user:
            return {'message': 'User not found'}, 404
        transactions = user.find_self_transactions()
        return {
            'message': 'Success',
            'data': [t.to_dict() for t in transactions]
        }, 200
