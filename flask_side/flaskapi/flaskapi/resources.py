# from datetime import datetime

from flask import request

from flask_restful import Resource

from flaskapi.flaskapi.request_parsers import login_parser


class Home(Resource):
    def get(self):
        return {'Hello': 'World'}


class Login(Resource):
    pass


class User(Resource):
    pass


class Deposit(Resource):
    pass


class Withdraw(Resource):
    pass


class Transfer(Resource):
    pass


class Statements(Resource):
    pass
