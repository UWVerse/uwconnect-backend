import json
from flask import Blueprint, request, jsonify
from apifairy import response,body, other_responses, arguments
from mongoengine import ValidationError
from werkzeug.exceptions import BadRequest, NotFound

from uwconnect_core.main.model.user import User, UserCredential
from uwconnect_core.main.service.utils import *
from uwconnect_core.main.api.schemas.shared_schema import MessageSchema
from uwconnect_core.main.api.schemas.user_schema import UserSchema, UserAuthorizeSchema, UserDetailRequestSchema, UserCredentailSchema

user = Blueprint('user', __name__)
message_schema = MessageSchema()
user_cre_schema = UserCredentailSchema()
user_schema = UserSchema()
user_authorize_schema = UserAuthorizeSchema()
user_request_schema = UserDetailRequestSchema()

@user.route("/register", methods=['POST'])
@body(user_cre_schema)
@response(message_schema)
@other_responses({500: 'server error'})
def register(request):
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
    userData = document_to_dict(request)
    user = UserCredential(**userData)
    if UserCredential.objects(email=user.email).count() != 0:
        raise BadRequest("exist")
        
    try:
        user.validate()
    except ValidationError as e:
        print(e)
        raise BadRequest("invalid arguments")
    
    user.save()
    return { "message": "success" }


# @user.route("/validate", methods=['POST'])
@user.post("/validate")
@body(user_authorize_schema)
@response(message_schema)
@other_responses({500: 'server error'})
def validate(request):
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

    data = request
    user_email = data['email']
    user_password = data['password']
    flag_checkUserOnly = data['checkUserOnly']

    # objects.get() is used when you are pretty sure that there is only one result. 
    # But its better to use objects.filter().first(), because it won't cause any errors. 
    if flag_checkUserOnly:
        user_query = UserCredential.objects.filter(email=user_email).first()
    else:
        user_query = UserCredential.objects.filter(email=user_email,password=user_password).first()
    
    if(user_query):
        return { "message": "exist" } if flag_checkUserOnly else { "message": "success" }
    else:
        return { "message": "fail" }

@user.route("/profile", methods=['GET'])
@arguments(user_request_schema)
@response(user_schema)
def getProfile(request):
    """
    GET user profile
        Incoming request message:
            query parameter: ?email=<email address>

        Return message:
            if email does not exist: { "message": "user does not exist" }
            otherwise: { "message": "success", "body": <user object> }
    """
    # args = request.get("email")
    email = request.get("email")
    user = User.objects.filter(email=email)

    if user.count() == 0:
        raise NotFound("user does not exist")
    
    userDetail = user().first()

    return userDetail
    
@user.route("/profile", methods=['POST'])
@body(user_schema)
@response(message_schema)
def updateProfile(request):
    """
    POST: update user detail
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
    user_email = request.email
    user_query = UserCredential.objects.filter(email=user_email)
    if (user_query.count() == 0):
        raise BadRequest("Account does not exist")
    try:
        request.validate_profile()
    except ValidationError:
        raise BadRequest("invalid arguments")
    
    if User.objects(email=user_email).modify(upsert=True, new=True, **document_to_dict(request)):
        return { "message": "success" }
    raise NotFound("user does not exist")
    