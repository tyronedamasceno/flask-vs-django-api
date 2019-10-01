from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ultra-secret-string'

db = SQLAlchemy(app)

from flaskapi.flaskapi import resources
from flaskapi.flaskapi import models

# db.drop_all()
db.create_all()

# from flaskapi.flaskapi import populate_db
# # populate_db.populate()

api.add_resource(resources.Home, '/')
api.add_resource(resources.Login, '/login')
api.add_resource(resources.User, '/user')
api.add_resource(resources.Deposit, '/deposit')
api.add_resource(resources.Withdraw, '/withdraw')
api.add_resource(resources.Transfer, '/transfer')
api.add_resource(resources.Statements, '/statements')
