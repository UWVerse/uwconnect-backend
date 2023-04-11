from marshmallow import validate, validates, validates_schema, ValidationError, post_dump
import marshmallow_mongoengine as ma
from uwconnect_core.main import flaskMarshal

class MessageSchema(flaskMarshal.Schema):
    class Meta:
        ordered = True
    message = flaskMarshal.String()

class EmptySchema(flaskMarshal.Schema):
    pass