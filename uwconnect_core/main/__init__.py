import flask
from flask import Flask, jsonify, redirect, session, url_for
#from flask_cors import cross_origin
from pymongo import MongoClient
from datetime import datetime, timedelta
from mongoengine import *
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
import configparser
from flask_session import Session
from uwconnect_core.main.service.utils import get_file_path
from uwconnect_core.main.service.load_enrollment_db import load_enrollment
from uwconnect_core.main.service.load_hobbies_db import load_hobbies

flaskMarshal = Marshmallow()
apifairy = APIFairy()
sess = Session()

def create_app(testing=False):
    """
    testing=False: normal run
    testing=True: used by unit tests. config.ini has to be the same mode as parameter.
    """

    app = Flask(__name__)
    # https://flask.palletsprojects.com/en/2.2.x/api/#flask.current_app
    with app.app_context():
        from uwconnect_core.main.api.user.routes import user
        from uwconnect_core.main.api.enrollment.routes import enrollment
        from uwconnect_core.main.api.hobbies.routes import hobbies
        from uwconnect_core.main.api.cometchat_webhook.routes import cometchat_webhook

        app.register_blueprint(user, url_prefix='/user')
        app.register_blueprint(enrollment, url_prefix="/enrollment")
        app.register_blueprint(hobbies, url_prefix="/hobbies")
        app.register_blueprint(cometchat_webhook, url_prefix="/cometchat_webhook")

        import uwconnect_core.main.handler  # Do NOT remove

    config = configparser.ConfigParser()
    config_path = get_file_path('config.ini')
    config.read(config_path)    
    mode = config['GLOBAL']['MODE']
    load_enrollment_db = True if config['GLOBAL']['LOAD_ENROLLMENT_DB'] == "True" else False
    load_dummy_db = True if config['GLOBAL']['LOAD_DUMMY_DB'] == "True" else False

    if testing and mode != 'TEST':
        raise ValueError(mode, 'mode of the database is not allowed for running unit test.')

    connect(host=config[mode]['DB_URI'])
    
    if load_enrollment_db:
        # Insert a list of courses, programs, faculty into database
        load_enrollment(config[mode]['UW_API_KEY'])
        # Insert a list of pre-define tag into database
        load_hobbies()

    if load_dummy_db:
        from uwconnect_core.main.service.load_dummy_db import load_dummy_users, delete_all_user
        delete_all_user()
        load_dummy_users(num_users=100, create_test_user=True, tags=['Tennis'],
                            courses=['ECE650', 'ECE651'],
                            faculty = 'Engineering',
                            profile_visible=True)
    
    app.config['APIFAIRY_TITLE'] = 'UW Connect API'
    app.config['APIFAIRY_VERSION'] = '1.0'
    app.config['APIFAIRY_UI'] = 'swagger_ui'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["SESSION_USE_SIGNER"] = True
    app.config['SECRET_KEY'] = config[mode]['SECRET_KEY']
    app.config['SESSION_COOKIE_SECURE'] = True if config[mode]['SESSION_COOKIE_SECURE'] == 'True' else False
    app.config['SESSION_COOKIE_SAMESITE'] = 'none'
    app.config['FRONTEND_DOMAIN'] = config[mode]['FRONTEND_DOMAIN']
    app.config['COMETCHAT_API_KEY'] = config[mode]['COMETCHAT_API_KEY']
    app.config['COMETCHAT_APP_ID'] = config[mode]['COMETCHAT_APP_ID']
    # app.config['SESSION_COOKIE_DOMAIN'] = 'dev.localhost'

    flaskMarshal.init_app(app)
    apifairy.init_app(app)
    sess.init_app(app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=30)
    
    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))
    
    return app
