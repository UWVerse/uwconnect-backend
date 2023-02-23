from flask import Blueprint
from flask import jsonify
from datetime import datetime
from apifairy import arguments,response, other_responses
from uwconnect_core.main.api.schemas.shared_schema import MessageSchema

dummy = Blueprint('dummy', __name__)
message_schema = MessageSchema()
@dummy.route('/test')
@response(message_schema)
@other_responses({500: 'server error'})
def root():
    """Dummy API for testing"""
    message = 'This page has been visited 1 times'
    return { 'message': message }