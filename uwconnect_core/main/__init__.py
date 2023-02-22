import flask
from flask import Flask, jsonify, redirect, url_for
#from flask_cors import cross_origin
from pymongo import MongoClient
from datetime import datetime
from mongoengine import *
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
import configparser
import os

flaskMarshal = Marshmallow()
config = configparser.ConfigParser()
config.read(os.path.abspath("config.ini"))
app = Flask(__name__)
apifairy = APIFairy()
mode = config['GLOBAL']['MODE']
connect(host=config[mode]['DB_URI'])


def create_app():

    from uwconnect_core.main.api.dummy.routes import dummy
    from uwconnect_core.main.api.user.routes import user

    app.register_blueprint(dummy, url_prefix='/dummy')
    app.register_blueprint(user, url_prefix='/user')

    from uwconnect_core.main.handler import handle_bad_request
    app.config['APIFAIRY_TITLE'] = 'UW Connect API'
    app.config['APIFAIRY_VERSION'] = '1.0'
    app.config['APIFAIRY_UI'] = 'swagger_ui'
    flaskMarshal.init_app(app)
    apifairy.init_app(app)

    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))
    
    return app
