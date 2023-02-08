import flask
from flask import Flask, jsonify
#from flask_cors import cross_origin
from pymongo import MongoClient
from datetime import datetime
from flask_pymongo import PyMongo
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.abspath("config.ini"))

app = Flask(__name__)
client = PyMongo(app, uri=config['PROD']['DB_URI']) 
db = client.db


def create_app():

    from uwconnect_core.api.dummy.routes import dummy
    # from uwconnect_core.api.users.routes import users

    app.register_blueprint(dummy, url_prefix='/dummy')
    # app.register_blueprint(users, url_prefix='/users')


    return app
