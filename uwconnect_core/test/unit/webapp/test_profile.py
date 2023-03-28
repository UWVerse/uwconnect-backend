"""
To use the client fixture we created in webapp __init__.py, 
we need to import it. PyCharm will claim that the import is unused, but pytest actually needs it. 
"""
from uwconnect_core.test.unit.webapp import client
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

def test_get_profile(client):
    """
    GET user profile
        Incoming request message:
            query parameter: ?email=<email address>

        Return message:
            if email does not exist: { "message": "user does not exist" }
            otherwise: { "message": "success", "body": <user object> }
    """
    delete_all_user()
    test_user = load_test_user() #email equal to test@uwaterloo.ca

    # Fake session without going through the login route
    with client.session_transaction() as session:
        session["email"] = 1

    # email exist
    response = client.get('/user/profile?email=test@uwaterloo.ca')
    code = response.status_code
    assert code == 200

    # if email does not exist
    response = client.get('/user/profile?email=xxx@uwaterloo.ca')
    code = response.status_code
    assert code == 404
    
    delete_user_by_doc(test_user)

def test_post_profile(client):
    """
    POST: update user detail
    @body(user_schema)
    @response(message_schema)
    """
    delete_all_user()
    test_user = load_test_user() #email equal to test@uwaterloo.ca
    
    # TODO

    delete_user_by_doc(test_user)