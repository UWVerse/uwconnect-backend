from uwconnect_core.main.handler.error_handler import *
from uwconnect_core.main import app

app.register_error_handler(BadRequest, handle_bad_request)
