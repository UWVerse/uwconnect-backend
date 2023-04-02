from werkzeug.exceptions import BadRequest, InternalServerError, NotFound, Forbidden, Unauthorized


def handle_bad_request(e: BadRequest):
    return { "message": e.description }, 400

def handle_unauthorized_error(e: Unauthorized):
    return { "message": e.description }, 403

def handle_forbidden_error(e: Forbidden):
    return { "message": e.description }, 403


def handle_not_found_error(e: NotFound):
    return { "message": e.description }, 404


def handle_internal_server_error(e: InternalServerError):
    return { "message": f"unexpected error" }, 500
