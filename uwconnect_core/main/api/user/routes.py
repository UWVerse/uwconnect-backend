from flask import Blueprint, request
from mongoengine import ValidationError
from werkzeug.exceptions import BadRequest

from uwconnect_core.main.model.user import User

user = Blueprint('user', __name__)

@user.route("/register", methods=['POST'])
def ping_db():
    user = User(**request.get_json())
    if User.objects(email=user.email).count() != 0:
        raise BadRequest("user existed")
        
    try:
        user.validate()
    except ValidationError:
        raise BadRequest("invalid arguments")
    
    user.save()
    return { "message": "success" }