from uwconnect_core.main.model.enrollment import Enrollment
import marshmallow_mongoengine as ma
from uwconnect_core.main.service.utils import *
from flask import jsonify


class EnrollmentSchema(ma.ModelSchema):
    class Meta:
        model = Enrollment

    def jsonify(self, data):
        result = document_to_dict(data)
        return jsonify(result)