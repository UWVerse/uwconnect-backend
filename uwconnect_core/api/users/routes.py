from uwconnect_core import db
from flask import Blueprint
from flask import jsonify
from datetime import datetime

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
#@cross_origin()
def root():
    db.hits.insert_one({ 'time': datetime.utcnow() })
    message = 'This page has been visited {} times.'.format(db.hits.count_documents({ 'time': datetime.utcnow() }))
    return jsonify({ 'message': message })

@users.route("/ping_db", methods=['GET'])
def ping_db():
    Test = db.Test.find()
    print(123123123)
    return jsonify([Test for Test in Test])