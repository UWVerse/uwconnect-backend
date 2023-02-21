import flask
from flask import Flask, jsonify
#from flask_cors import cross_origin
from pymongo import MongoClient
from datetime import datetime
from mongoengine import *

import configparser
import os

app = Flask(__name__)

"""
blueprint should be declared globally
see # https://github.com/pallets/flask/issues/4786
"""
#======================================================
from uwconnect_core.main.api.dummy.routes import dummy
from uwconnect_core.main.api.user.routes import user
from uwconnect_core.main.handler import handle_bad_request
app.register_blueprint(dummy, url_prefix='/dummy')
app.register_blueprint(user, url_prefix='/user')
#======================================================

def create_app(testing=False):
    """
    testing=False: normal run
    testing=True: used by unit tests. config.ini has to be the same mode as parameter.
    """
    config = configparser.ConfigParser()
    config_path = get_config_path('config.ini')
    config.read(config_path)    
    mode = config['GLOBAL']['MODE']
    if testing and mode != 'TEST':
        raise ValueError(mode, 'mode of the database is not allowed for running unit test.')

    connect(host=config[mode]['DB_URI'])

    return app

def get_config_path(filename):
    """
    search config.ini file across whole repo and return abspath
    """
    for root, dirs, files in os.walk(r'.'):
        for name in files:
            if name == filename:
                return os.path.abspath(os.path.join(root, name))
    raise FileNotFoundError("config.ini not found. You have to create one and fill in the secret key. Take config.ini.example as a reference.")