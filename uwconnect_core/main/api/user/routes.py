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


@user.route("/login", methods=['POST'])
def login():
    """
    Incoming request message:
    username/password as parameter - all will be encoded before send
    checkUserOnly flag as parameter - if this flag enable, we will check if user account exist only.

    Return message:
    process to check if username+password combination is valid
    if checkUserOnly flag is off: return “success” if its valid account
    if checkUserOnly flag is on: return “existing” if its valid account
    return “fail“ if its invalid account
    """

    data = request.get_json()
    user_email = data['email']
    user_password = data['password']
    flag_checkUserOnly = data['checkUserOnly']

    # objects.get() is used when you are pretty sure that there is only one result. 
    # But its better to use objects.filter().first(), because it won't cause any errors. 
    if flag_checkUserOnly:
        user_query = User.objects.filter(email=user_email).first()
    else:
        user_query = User.objects.filter(email=user_email,password=user_password).first()
    
    if(user_query):
        return { "message": "existing" } if flag_checkUserOnly else { "message": "success" }
    else:
        return { "message": "fail" }
    