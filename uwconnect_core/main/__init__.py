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
from uwconnect_core.main.service.utils import get_file_path
from uwconnect_core.main.service.load_enrollment_db import load_enrollment
from uwconnect_core.main.service.load_hobbies_db import load_hobbies

app = Flask(__name__)
flaskMarshal = Marshmallow()
apifairy = APIFairy()

"""
blueprint should be declared globally
see # https://github.com/pallets/flask/issues/4786
"""
from uwconnect_core.main.api.user.routes import user
from uwconnect_core.main.api.enrollment.routes import enrollment
from uwconnect_core.main.api.hobbies.routes import hobbies

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(enrollment, url_prefix="/enrollment")
app.register_blueprint(hobbies, url_prefix="/hobbies")

import uwconnect_core.main.handler  # Do NOT remove


def create_app(testing=False):
    """
    testing=False: normal run
    testing=True: used by unit tests. config.ini has to be the same mode as parameter.
    """
    config = configparser.ConfigParser()
    config_path = get_file_path('config.ini')
    config.read(config_path)    
    mode = config['GLOBAL']['MODE']
    load_enrollment_db = True if config['GLOBAL']['LOAD_ENROLLMENT_DB'] == "True" else False
    if testing and mode != 'TEST':
        raise ValueError(mode, 'mode of the database is not allowed for running unit test.')

    connect(host=config[mode]['DB_URI'])
    
    if load_enrollment_db:
        # Insert a list of courses, programs, faculty into database
        load_enrollment(config[mode]['UW_API_KEY'])
        # Insert a list of pre-define tag into database
        load_hobbies()

    app.config['APIFAIRY_TITLE'] = 'UW Connect API'
    app.config['APIFAIRY_VERSION'] = '1.0'
    app.config['APIFAIRY_UI'] = 'swagger_ui'
    flaskMarshal.init_app(app)
    apifairy.init_app(app)
    
    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))
    
    return app
