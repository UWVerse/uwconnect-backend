"""
To use the client fixture we created in webapp __init__.py, 
we need to import it. PyCharm will claim that the import is unused, but pytest actually needs it. 
"""
from uwconnect_core.test.unit.webapp import client
# https://codethechange.stanford.edu/guides/guide_flask_unit_testing.html
# https://flask.palletsprojects.com/en/2.2.x/testing/

from uwconnect_core.main.service.load_dummy_db import *
from uwconnect_core.main.service.dummy_factory import *
from uwconnect_core.main.service.recommendation_system import *

# Need not to run `server.py`
# Directly run `python -m pytest`

def test_recommendation(client):
    user = RandomUserFactory(username="test",
                             tags=['Tennis'],
                             profile_visible=True)
    records = search_recommendation_db(user)
    print(records)