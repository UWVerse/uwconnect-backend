from flask import Blueprint, request, jsonify
from apifairy import response, body, other_responses, arguments
from werkzeug.exceptions import BadRequest, NotFound

from uwconnect_core.main.model.enrollment import Enrollment
from uwconnect_core.main.api.schemas.enrollment_schema import EnrollmentSchema

enrollment = Blueprint('enrollment', __name__)
enrollment_schema = EnrollmentSchema()


@enrollment.route("/", methods=['GET'])
@response(enrollment_schema)
def index():
    """
    GET list of faculties, prorgams, courses
    """
    return Enrollment.objects().first()