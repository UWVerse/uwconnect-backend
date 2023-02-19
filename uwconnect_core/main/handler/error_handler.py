from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError


def handle_bad_request(e: BadRequest):
    return { "message": e.description }, 400


def handle_internal_server_error(e: InternalServerError):
    return { "message": "unexpected error" }, 500

