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
import uwconnect_core.main.service.cometchat_api as cometchat_api
import pytest

# Need not to run `server.py`
# Directly run `python -m pytest`
# Directly run `python -m pytest -v -s --disable-warnings`

def test_register_status_code(client):
    """
    check if status code of /user/register is not allowed (Code 405)
    """
    assert client.get("/user/register").status_code == 405

def test_validate_status_code(client):
    """
    check if status code of /user/validate is not allowed (Code 405)
    """
    assert client.get("/user/validate").status_code == 405


def test_user_register(client):
    """
    Test the register
    return HTTP: 200 “success” if account created successfully
    return HTTP: 200 “exist“ if account is exist
    return server error if there is other error occurred
    """
    user_info = {
                    "email": "xxx@uwaterloo.ca",
                    "password": "xxxx",
                }
    
    user_info_wrong_pw = {
                    "email": "xxx@uwaterloo.ca",
                    "password": "wrong",
    }

    # Incase the data exists in the database
    query = UserCredential.objects.filter(email=user_info['email'], password=user_info['password']).first()
    if query:
        query.delete()
    assert UserCredential.objects(email=user_info['email'], password=user_info['password']).count() == 0

    #account created successfully
    response = client.post('/user/register', json=user_info)
    message = response.data.decode()
    assert "success" in message

    #account existed (with same password)
    response = client.post('/user/register', json=user_info)
    message = response.data.decode()
    assert "exist" in message

    #account existed (with different password)
    response = client.post('/user/register', json=user_info_wrong_pw)
    message = response.data.decode()
    assert "exist" in message

    # delete the added dummy data
    query = UserCredential.objects.filter(email=user_info['email'], password=user_info['password']).first()
    if query:
        query.delete()
    assert UserCredential.objects(email=user_info['email'], password=user_info['password']).count() == 0
    
def test_user_register_exist(client, test_user_with_cred):
    """
    Test the register
    return HTTP: 200 “success” if account created successfully
    return HTTP: 200 “exist“ if account is exist
    return server error if there is other error occurred
    """
    user, user_cred = test_user_with_cred
    user_info = {
                "email": user_cred.email,
                "password": user_cred.password,
            }
    response = client.post('/user/register', json=user_info)
    message = response.data.decode()
    assert "exist" in message
    
def test_user_validate(logged_in_client):
    """
    validation process to check if username+password combination is valid
    if checkUserOnly flag is off: return “success” if its valid account
    if checkUserOnly flag is on: return “existing” if its valid account
    return “fail“ if its invalid account
    """

    client = logged_in_client
    user_info = {
                    "email": "xxx@uwaterloo.ca",
                    "password": "xxxx",
                }
    #account created successfully
    response = client.post('/user/register', json=user_info)

    # if checkUserOnly flag is off: return “success” if its valid account
    response = client.post('/user/validate', json={
                    "email": "xxx@uwaterloo.ca",
                    "password": "xxxx",
                    "checkUserOnly": False,
                })
    message = response.data.decode()
    assert "incomplete profile" in message

    # if checkUserOnly flag is on: return “existing” if its valid account
    response = client.post('/user/validate', json={
                    "email": "xxx@uwaterloo.ca",
                    "password": "xxxx",
                    "checkUserOnly": True,
                })
    message = response.data.decode()
    assert "exist" in message

    response = client.post('/user/validate', json={
                    "email": "xxx@uwaterloo.ca",
                    "password": "xxxx22",
                    "checkUserOnly": False,
                })
    message = response.data.decode()
    assert "fail" in message

    response = client.post('/user/validate', json={
                    "email": "xxx2222@uwaterloo.ca",
                    "password": "xxxx",
                    "checkUserOnly": True,
                })
    message = response.data.decode()
    assert "fail" in message

    # delete the added dummy data
    query = UserCredential.objects.filter(email=user_info['email'], password=user_info['password']).first()
    if query:
        query.delete()
    assert UserCredential.objects(email=user_info['email'], password=user_info['password']).count() == 0


def test_check_friends(logged_in_client, test_cometchat_user, mock_friends):
    """
    Test the check friends
    return HTTP: 200 “success” if account created successfully
    return HTTP: 200 “exist“ if account is exist
    return server error if there is other error occurred
    """
    # Test if the users are not friends
    client = logged_in_client
    non_friend = test_cometchat_user
    friend_a, friend_b = mock_friends
    response = client.get(f'/user/check_friends?me={non_friend.email}&other={friend_a.email}')
    
    assert response.status_code == 200
    message = response.data.decode()
    assert "false" in message
    
    # Test if the users are friends
    response = client.get(f'/user/check_friends?me={friend_a.email}&other={friend_b.email}')
    assert response.status_code == 200
    message = response.data.decode()
    assert "true" in message
    
    # Test if the user does not exist
    response = client.get(f'/user/check_friends?me=i_dont_exist&other={friend_b.email}')
    assert response.status_code != 200

    
    
