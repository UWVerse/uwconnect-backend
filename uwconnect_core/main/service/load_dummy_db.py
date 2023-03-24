from uwconnect_core.main.model.user import *
from uwconnect_core.main.service.dummy_factory import RandomUserFactory, RandomUserCredentialFactory
from faker import Faker
import random

def load_dummy_users(num_users=500, create_test_user=False, **kwarg):
    """
    Generate User and UserCredential in a number of `num_users` in the database.
    create_test_user: True -> Generate a test user with email=test@uwaterloo.ca, password=12345678
    kwarg: is for arguments of RandomUserFactory, i.e. tags, courses
    """
    if create_test_user:
        load_test_user(**kwarg)
    # Generate `num_users` users
    fake = Faker()
    for i in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name.lower()}{last_name.lower()}{random.randint(0,10)}'
        email = f'{username}@uwaterloo.ca'
        user = RandomUserFactory(first_name=first_name, last_name=last_name, username=username, email=email)
        user_cred = RandomUserCredentialFactory(email=email)
    # By recreating the object, User is already added to the Database


def delete_all_user():
    """
    Dropping mongo db collection of User and UserCredential.
    Use with caution. 
    """
    User.drop_collection()
    UserCredential.drop_collection()

def load_test_user(username="test", password="12345678", get_cred=False, **kwarg):
    """
    Load test user.
    **kwarg is for arguments of RandomUserFactory, i.e. tags, courses
    """
    username = "test"
    #user = RandomUserFactory(username=username,
    #                        tags=['Tennis'],
    #                        courses=['ECE650', 'ECE651'],
    #                        faculty = 'Engineering',
    #                        profile_visible=True)
    email = f'{username}@uwaterloo.ca'
    user = RandomUserFactory(username=username, email=email, **kwarg)
    user_cred = RandomUserCredentialFactory(email=email, password=password)

    if get_cred:
        return user, user_cred
    else:
        return user