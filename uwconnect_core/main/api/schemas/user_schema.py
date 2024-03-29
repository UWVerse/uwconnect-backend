from marshmallow import validate, validates, validates_schema, ValidationError, post_dump
# from uwconnect_core.main import ma
from uwconnect_core.main.model.user import User, UserCredential
import marshmallow_mongoengine as ma
from uwconnect_core.main import flaskMarshal
from flask import jsonify
from uwconnect_core.main.service.utils import *

class UserCredentialSchema(ma.ModelSchema):
    class Meta:
        model = UserCredential
    
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        ordered = True

    def jsonify(self, data):
        result = document_to_dict(data)
        return jsonify(result)
    

class UserAuthorizeSchema(flaskMarshal.Schema):
    class Meta:
        ordered = True
    email = flaskMarshal.String()
    password = flaskMarshal.String()
    checkUserOnly = flaskMarshal.Boolean()


class SessionSchema(flaskMarshal.Schema):
    username = flaskMarshal.String()
    email = flaskMarshal.String()


class UserEmailSchema(flaskMarshal.Schema):
    email = flaskMarshal.String()
    
class UserFriendEmailSchema(flaskMarshal.Schema):
    me = flaskMarshal.String()
    other = flaskMarshal.String()
    
class UserFilterSchema(ma.ModelSchema):
    class Meta:
        model = User
        ordered = True
        fields = ["gender","faculty","program","courses","tags"]

class UserListSchema(flaskMarshal.Schema):
    class Meta:
        ordered = True
    users = flaskMarshal.List(flaskMarshal.Nested(UserSchema))
    total = flaskMarshal.Integer()

class CometchatUidListSchema(flaskMarshal.Schema):
    class Meta:
        ordered = True
    emails = flaskMarshal.List(flaskMarshal.String())