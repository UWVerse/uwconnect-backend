import json
from flask import Blueprint, request
from mongoengine import ValidationError
from werkzeug.exceptions import BadRequest, NotFound

from uwconnect_core.main.model.user import User
from uwconnect_core.main.service.utils import *

user = Blueprint('user', __name__)

@user.route("/register", methods=['POST'])
def register():
    """
    Incoming request message:
    username/password as parameter - all will be encoded before send
    
    * need to check if the username already exist in database.
    * if the username is new then process to save the username and password to database. 
    * the account should have status as unverified.

    Return message:
    return HTTP: 200 { "message": "success" } if account created successfully
    return HTTP: 200 { "message": "exist" } if account is exist
    return server error if there is other error occurred
    """
    user = User(**request.get_json())
    if User.objects(email=user.email).count() != 0:
        raise BadRequest("exist")
        
    try:
        user.validate()
    except ValidationError:
        raise BadRequest("invalid arguments")
    
    user.save()
    return { "message": "success" }


@user.route("/validate", methods=['POST'])
def validate():
    """
    Incoming request message:
    username/password as parameter - all will be encoded before send
    checkUserOnly flag as parameter - if this flag enable, we will check if user account exist only.

    Return message:
    process to check if username+password combination is valid
    if checkUserOnly flag is off: return { "message": "success" } if its valid account
    if checkUserOnly flag is on: return { "message": "exist" } if its valid account
    return { "message": "fail" } if its invalid account
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
        return { "message": "exist" } if flag_checkUserOnly else { "message": "success" }
    else:
        return { "message": "fail" }


@user.route("/profile", methods=['GET', 'POST'])
def profile():
    """
    GET:
        Incoming request message:
            query parameter: ?email=<email address>

        Return message:
            if email does not exist: { "message": "user does not exist" }
            otherwise: { "message": "success", "body": <user object> }

    POST:
        Incoming request message:
            body: {
                email = EmailField(domain_whitelist=["@uwaterloo.ca"], required="true")
                username = StringField(regex="[A-Za-z0-9_ ]+", min_length=6, max_length=32)
                gender = StringField(max_length=16)
                faculty = StringField()
                program = StringField()
                year = IntField()
                courses = ListField(StringField(regex="[A-Z]+[0-9]+[A-Z]*"))
                tags = ListField(StringField())
                bio = StringField(max_length=1024)
            }

        Return Message:
            if request body does not follow the above structure: "invalid arguments"
            if email does not exist: { "message": "user does not exist" }
            otherwise: { "message": "success" }

    """
    if request.method == "GET":
        args = request.args
        email = args.get("email")
        user = User.objects.filter(email=email)

        if user.count() == 0:
            raise NotFound("user does not exist")
        
        user = document_to_dict(user().first())
        user.pop("password")
        user.pop("_id")
        return { "message": "success", "body": user }

    else:
        profile = User(**request.get_json())
        email = profile.email
        print(email)

        try:
            profile.validate_profile()
        except ValidationError:
            raise BadRequest("invalid arguments")
        
        if User.objects(email=email).modify(**request.get_json()):
            return { "message": "success" }
        raise NotFound("user does not exist")
    