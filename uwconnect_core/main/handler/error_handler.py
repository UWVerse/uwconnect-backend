from werkzeug.exceptions import BadRequest, InternalServerError, NotFound


def handle_bad_request(e: BadRequest):
    return { "message": e.description }, 400


def handle_internal_server_error(e: InternalServerError):
    return { "message": "unexpected error" }, 500


def handle_not_found_error(e: NotFound):
    return { "message": e.description }, 404

