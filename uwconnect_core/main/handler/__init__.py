from uwconnect_core.main.handler.error_handler import *
from uwconnect_core.main import app

app.register_error_handler(BadRequest, handle_bad_request)
app.register_error_handler(InternalServerError, handle_internal_server_error)
app.register_error_handler(NotFound, handle_not_found_error)
