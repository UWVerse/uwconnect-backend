from uwconnect_core.main.model.hobbies import Hobbies
import marshmallow_mongoengine as ma
from uwconnect_core.main.service.utils import *
from flask import jsonify


class HobbiesSchema(ma.ModelSchema):
    class Meta:
        model = Hobbies

    def jsonify(self, data):
        result = document_to_dict(data)
        return jsonify(result)