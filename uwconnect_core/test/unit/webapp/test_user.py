"""
To use the client fixture we created in webapp __init__.py, 
we need to import it. PyCharm will claim that the import is unused, but pytest actually needs it. 
"""
from uwconnect_core.test.unit.webapp import client
# https://codethechange.stanford.edu/guides/guide_flask_unit_testing.html
# https://flask.palletsprojects.com/en/2.2.x/testing/

# Need not to run `server.py`
# Directly run `python -m pytest`

def test_status_code(client):
    """
    check if status code of /user/... are not allowed (Code 405)
    """
    api_status_405 =  [ 
                client.get("/user/register").status_code, 
                client.get("/user/validate").status_code, 
                ]
    # Check status for 405 not allowed
    for code in api_status_405:
        assert code == 405

# How can I fake request.POST and GET params for unit testing in Flask?
# https://stackoverflow.com/questions/7428124/how-can-i-fake-request-post-and-get-params-for-unit-testing-in-flask

def test_user_register(client):
    """
    Test the register
    return HTTP: 200 “success” if account created successfully
    return HTTP: 200 “exist“ if account is exist
    return server error if there is other error occurred
    """
    from uwconnect_core.main.model.user import User
    user_info = {
                    "email": "xxx@uwaterloo.ca",
                    "password": "xxxx",
                }
    
    user_info_wrong_pw = {
                    "email": "xxx@uwaterloo.ca",
                    "password": "wrong",
    }

    bad_info = {
                    "email": "xxx@uoft.ca",
                    "password": "xxxx",
    }

    # Incase the data exists in the database
    query = User.objects.filter(email=user_info['email'], password=user_info['password']).first()
    if query:
        query.delete()
    assert User.objects(email=user_info['email'], password=user_info['password']).count() == 0

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
    query = User.objects.filter(email=user_info['email'], password=user_info['password']).first()
    if query:
        query.delete()
    assert User.objects(email=user_info['email'], password=user_info['password']).count() == 0
    
def test_user_validate(client):
    """
    validation process to check if username+password combination is valid
    if checkUserOnly flag is off: return “success” if its valid account
    if checkUserOnly flag is on: return “existing” if its valid account
    return “fail“ if its invalid account
    """

    from uwconnect_core.main.model.user import User
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
    assert "success" in message

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
    query = User.objects.filter(email=user_info['email'], password=user_info['password']).first()
    if query:
        query.delete()
    assert User.objects(email=user_info['email'], password=user_info['password']).count() == 0