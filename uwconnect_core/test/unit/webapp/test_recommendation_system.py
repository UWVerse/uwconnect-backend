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
from uwconnect_core.main.service.utils import *

import logging

# Need not to run `server.py`
# Directly run `python -m pytest`
# Directly run `python -m pytest -v -s --disable-warnings`

def test_recommendation(client):
    
    delete_all_user()
    load_dummy_users(50)
    user = RandomUserFactory(username="test",
                             tags=['Tennis'],
                             profile_visible=True)
    records = search_recommendation_db(user)
    print("len(records): ", len(records))
    assert len(records) > 0

    recommendations = get_recommendation(user, records, list_length=10, score_threshold=10)
    print("len(recommendations): ", len(recommendations))
    assert len(recommendations) > 0

    print(document_to_dict(user))
    print(document_to_dict(recommendations[0]))
    """
    print(user.courses)
    print(user.tags)
    print(recommendations[0].tags)
    print(recommendations[0].courses)
    """

