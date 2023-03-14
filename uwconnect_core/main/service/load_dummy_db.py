from uwconnect_core.main.model.user import *
from uwconnect_core.main.service.dummy_factory import RandomUserFactory

def load_dummy_users(num_users=500):
    # Generate `num_users` users
    for i in range(num_users):
        user = RandomUserFactory()
    # By recreating the object, User is already added to the Database

def delete_all_user():
    User.drop_collection()
