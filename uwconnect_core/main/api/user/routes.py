from flask import Blueprint, make_response, redirect, request, jsonify, session
from apifairy import response, body, other_responses, arguments

from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Unauthorized
from mongoengine import ValidationError, Q

from uwconnect_core.main.model.user import User, UserCredential
from uwconnect_core.main.service.user_service import check_login, cometchat_create_user, delete_session, get_session, pop_session, set_session
from uwconnect_core.main.service.recommendation_system import *
from uwconnect_core.main.service.utils import *
from uwconnect_core.main.api.schemas.shared_schema import MessageSchema
from uwconnect_core.main.api.schemas.user_schema import *
import uwconnect_core.main.service.cometchat_api as cometchat_api

user = Blueprint('user', __name__)
message_schema = MessageSchema()
user_cre_schema = UserCredentialSchema()
user_schema = UserSchema()
user_authorize_schema = UserAuthorizeSchema()
user_email_schema = UserEmailSchema()
session_schema = SessionSchema()
user_filter_schema = UserFilterSchema()
user_list_schema = UserListSchema()

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
    return { "message": "fail" } if its invalid account, return 403 Forbidden if the user's profile is incomplete
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
        profile_query = User.objects.filter(email=user_email)
    
    if(user_query):
        if flag_checkUserOnly:
            return { "message": "exist" } 
        elif profile_query:
            set_session("email", user_email)
            return { "message": "success" }
        else:
            # user registered but profile incomplete
            raise Forbidden("incomplete profile")
    else:
        return { "message": "fail" }


@user.route("/profile", methods=['GET'])
@arguments(user_email_schema)
@response(user_schema)
@check_login
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
    del userDetail.id

    return userDetail
    

@user.route("/profile", methods=['POST'])
@body(user_schema)
@response(message_schema)
def updateProfile(request):
    """
    POST: update user detail

    """
    user_email = request.email
    user_query = UserCredential.objects.filter(email=user_email)
    if (user_query.count() == 0):
        raise BadRequest("Account does not exist")
    try:
        request.validate_profile()
    except ValidationError:
        raise BadRequest("invalid arguments")
    
    user_profile_query = User.objects(email=user_email)

    # resp.set_cookie("email", request.email)
    # resp.set_cookie("username", request.username)
    set_session("email", request.email)
    set_session("username", request.username)

    if user_profile_query.count() == 0:
        # new user
        uid = request.email.split('@')[0]
        cometchat_create_user(uid, request.username)


    user_profile_query.modify(upsert=True, new=True, **document_to_dict(request))
    return { "message": "success" }


@user.route("/who", methods=["GET"])
@response(user_email_schema)
def get_logged_in_user():
    """redirect to frontend homepage if the client is not logged in"""
    print(session)
    try:
        return {
            "email": get_session("email")
        }
    except:
        # return redirect(app.config['FRONTEND_DOMAIN'] + '/')
        raise Unauthorized("client not logged in")
    

@user.route("/logout", methods=["POST"])
@body(user_email_schema)
@check_login
def log_out(request):
    """remove the backend session for incoming client, email in request body must match the one in client's session"""
    email = request["email"]
    user = get_session("email")

    print(email, user)

    if email != user:
        raise Unauthorized("client not logged in")
    
    pop_session("email")
    delete_session()

    data = { "message": "success" }
    json_data = json.dumps(data)
    response = make_response(json_data)
    response.delete_cookie("session")
    response.headers['Content-Type'] = 'application/json'
    
    return response


@user.route("/test_middlewire", methods=["GET"])
@check_login
def test_middlewire():
    """
    a simple route that demonstrate how 'check_login' middlewire works, add it to protect all APIs that needs to be protected.
    All endpoints protected by 'check_login' will return 403 if no user is logged in for that client
    """
    return {"message": "success"}


@user.route("/filter", methods=['POST'])
@body(user_filter_schema)
@response(user_list_schema)
@check_login
def get_filtered_users(request):
    query = None
    if request.gender:
        query = Q(gender=request.gender)
    if request.faculty:
        query &= Q(faculty=request.faculty)
    if request.program:
        query &= Q(program=request.program)
    if request.courses:
        query &= Q(courses__all=request.courses)
    if request.tags:
        query &= Q(tags__all=request.tags)
    user_list = UserListSchema()
    user_list.users = User.objects(query)
    return user_list

@user.route("/get_recommendation", methods=["POST"])
@body(user_schema)
@check_login
def recommendation(request):
    """
    Incoming request message:
    user_schema #request is the user object

    Return message:
    return a list of recommendation users documents as JSON aka a list of user_schema
    """
    user = request
    records = search_recommendation_db(user)
    recommendations = get_recommendation(user, records, list_length=10, score_threshold=10)
    return document_to_dict_batch(recommendations)

cometchat_uid_list_schema = CometchatUidListSchema()

@user.get("/friends")
@arguments(user_email_schema)
@response(cometchat_uid_list_schema)
def get_friends(request):
    email = request.get("email")
    user : User = User.objects().get(email=email)
    cc_friends = cometchat_api.get_friends(user.get_uid(), "")
    # Append '@uwaterloo.ca' to uids
    uids = [cf['uid'] + "@uwaterloo.ca" for cf in cc_friends]
    cometchat_uid_list_schema = CometchatUidListSchema()
    cometchat_uid_list_schema.emails = uids
    return cometchat_uid_list_schema

user_friend_email_schema = UserFriendEmailSchema()

@user.get("/check_friends")
@arguments(user_friend_email_schema)
@response(message_schema)
def check_friend(request):
    me_email = request.get("me")
    other_email = request.get("other")
    me = User.objects().get(email=me_email)
    other = User.objects().get(email=other_email)
    if cometchat_api.get_friends(me.get_uid(), other.get_uid()):
        return {"message": "true"}
    return {"message": "false"}
