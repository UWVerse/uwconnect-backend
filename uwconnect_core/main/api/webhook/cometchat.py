from flask import Blueprint, request
import uwconnect_core.main.service.cometchat_api as comet_api
from uwconnect_core.main.model.friend import FriendRequest
from uwconnect_core.main.model.user import User

cometchat_webhook = Blueprint('cometchat_webhook', __name__)

@cometchat_webhook.post("/before_message")
def before_message():
    """
    Add this webhook to CometChat server triggered by "before_message" event.
    It records a friend request when user A sends the first message to user B.
    The friend request is deemed to be accepted when user B replies back, and 
    the two users are added as friends on CometChat server.
    User A cannot send any further messages to user B until the friend request
    is accepted.
    A friend request is expired if user B does not reply back within 24 hours.
    """
    entities = request.get_json().get('data').get('data').get('entities')
    sender_uid = entities.get('sender').get('entity').get('uid')
    receiver_uid = entities.get('receiver').get('entity').get('uid')
    # Permit if they are already friends
    if comet_api.get_friends(sender_uid, receiver_uid):
        return {}
    
    friend_request = None
    sender = User.objects().get(email=f"{sender_uid}@uwaterloo.ca")
    receiver = User.objects().get(email=f"{receiver_uid}@uwaterloo.ca")
    # If it is the friend requestee replying back, then permit and add them as friends
    try:
        friend_request = FriendRequest.objects().get(requester=receiver, requestee=sender)
        comet_api.add_friends(sender_uid, receiver_uid)
        # remove the friend request
        friend_request.delete()
        return {}
    except FriendRequest.DoesNotExist:
        pass
    
    # If it is the friend requester sending further messages, then reject
    try:
        friend_request = FriendRequest.objects().get(requester=sender, requestee=receiver)
        return {"action": "do_not_propagate"}
    except FriendRequest.DoesNotExist:
        pass
    
    # The sender is sending the first message to the receiver, then add a friend request and permit
    friend_request = FriendRequest(requester=sender, requestee=receiver)
    friend_request.validate()
    friend_request.save()
    return {}