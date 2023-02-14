import flask
from flask import Flask, jsonify
#from flask_cors import cross_origin
from pymongo import MongoClient
from datetime import datetime
from mongoengine import *
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.abspath("config.ini"))

app = Flask(__name__)
mode = config['GLOBAL']['MODE']
connect(host=config[mode]['DB_URI'])


def create_app():

    from uwconnect_core.main.api.dummy.routes import dummy
    from uwconnect_core.main.api.user.routes import user

    app.register_blueprint(dummy, url_prefix='/dummy')
    app.register_blueprint(user, url_prefix='/user')

    from uwconnect_core.main.handler import handle_bad_request

    return app
