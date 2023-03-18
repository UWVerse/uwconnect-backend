from enum import Enum
from mongoengine import *
import datetime

from uwconnect_core.main.model.user import User

class FriendRequest(Document):
    requester = ReferenceField(User, required=True)
    requestee = ReferenceField(User, required=True)
    created = DateTimeField(default=datetime.datetime.utcnow, required=True)
    meta = {
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': 24*60*60}
        ]
    }