"""
To use the client fixture we created in webapp __init__.py, 
we need to import it. PyCharm will claim that the import is unused, but pytest actually needs it. 
"""
from uwconnect_core.test.unit.webapp import *
# https://codethechange.stanford.edu/guides/guide_flask_unit_testing.html
# https://flask.palletsprojects.com/en/2.2.x/testing/

from uwconnect_core.main.model.user import UserCredential
from uwconnect_core.main.service.load_dummy_db import *
from uwconnect_core.main.service.dummy_factory import *
from uwconnect_core.main.service.recommendation_system import *
from uwconnect_core.main.service.utils import *

# Need not to run `server.py`
# Directly run `python -m pytest`
# Directly run `python -m pytest -v -s --disable-warnings`

def test_get_profile(logged_in_client, test_user):
    """
    GET user profile
        Incoming request message:
            query parameter: ?email=<email address>

        Return message:
            if email does not exist: { "message": "user does not exist" }
            otherwise: { "message": "success", "body": <user object> }
    """
    
    # email exist
    response = logged_in_client.get(f'/user/profile?email={test_user.email}')
    code = response.status_code
    assert code == 200

    # if email does not exist
    response = logged_in_client.get('/user/profile?email=xxx@uwaterloo.ca')
    code = response.status_code
    assert code == 404


def test_post_profile(logged_in_client, test_user):
    """
    POST: update user detail
    @body(user_schema)
    @response(message_schema)
    """
    pass