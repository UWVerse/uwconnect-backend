from werkzeug.exceptions import BadRequest


def handle_bad_request(e: BadRequest):
    return { "message": e.description }, 400
