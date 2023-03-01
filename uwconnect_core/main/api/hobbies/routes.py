from flask import Blueprint, request, jsonify
from apifairy import response, body, other_responses, arguments
from werkzeug.exceptions import BadRequest, NotFound

from uwconnect_core.main.model.hobbies import Hobbies
from uwconnect_core.main.api.schemas.hobbies_schema import HobbiesSchema

hobbies = Blueprint('hobbies', __name__)
hobbies_schema = HobbiesSchema()


@hobbies.route("/", methods=['GET'])
@response(hobbies_schema)
def index():
    """
    GET list of hobbies
    """
    return Hobbies.objects().first()