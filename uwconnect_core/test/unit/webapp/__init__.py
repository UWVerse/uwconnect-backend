from uwconnect_core.main import create_app
from uwconnect_core.main.service.load_dummy_db import *
import uwconnect_core.main.service.cometchat_api as cometchat_api
import pytest

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to``True``.

"""

# The @pytest.fixture annotation tells pytest that the following function creates (using the yield command) an app for testing.
@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """
    app = create_app(testing=True)
    #app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        yield client
    
@pytest.fixture
def logged_in_client(client):
    """
    client with session.
    """
    # How can I fake request.POST and GET params for unit testing in Flask?
    # https://stackoverflow.com/questions/7428124/how-can-i-fake-request-post-and-get-params-for-unit-testing-in-flask
    with client.session_transaction() as session:
        session["email"] = 1
    yield client
    
@pytest.fixture
def test_user():
    """
    test user (will be automatically deleted after test)
    """
    user = load_test_user()
    yield user
    delete_user_by_doc(user)

@pytest.fixture
def test_user_with_cred():
    """
    test user (will be automatically deleted after test)
    """
    user, user_cred = load_test_user(get_cred=True)
    yield user, user_cred
    delete_user_by_doc(user)

@pytest.fixture
def test_cometchat_user():
    """
    test user (will be automatically deleted after test)
    """
    user = load_test_user()
    cometchat_api.add_user(user.get_uid(), user.first_name)
    yield user
    delete_user_by_doc(user)
    
@pytest.fixture
def test_users(request):
    """
    test user (will be automatically deleted after test)
    """
    users = []
    for user in request.param:
        users.append(load_test_user(**user))
    yield users
    for user in users:
        delete_user_by_doc(user)

@pytest.fixture
def mock_friends():
    """
    test user (will be automatically deleted after test)
    """
    friend_a : User = load_test_user('test_friend_a')
    friend_b : User = load_test_user('test_friend_b')
    cometchat_api.add_user(friend_a.get_uid(), friend_a.first_name)
    cometchat_api.add_user(friend_b.get_uid(), friend_b.first_name)
    cometchat_api.add_friends(friend_a.get_uid(), friend_b.get_uid())
    yield friend_a, friend_b
    cometchat_api.remove_friends(friend_a.get_uid(), friend_b.get_uid())
    cometchat_api.remove_user(friend_a.get_uid())
    cometchat_api.remove_user(friend_b.get_uid())
    delete_user_by_doc(friend_a)
    delete_user_by_doc(friend_b)