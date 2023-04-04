import threading
from flask import Blueprint, current_app, request
import uwconnect_core.main.service.cometchat_api as comet_api
from uwconnect_core.main.model.friend import FriendRequest
from uwconnect_core.main.model.user import User
from uwconnect_core.main.service.schedule_friend_request_expiry import create_friend_request_expiry_job

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
    # If the request is expired, drop the message
    try:
        friend_request = FriendRequest.objects().get(requester=receiver, requestee=sender)

        if not friend_request.approved and not friend_request.expired:
            comet_api.add_friends(sender_uid, receiver_uid)
            friend_request.modify(approved=True)

        if not friend_request.expired:
            return {}
    except FriendRequest.DoesNotExist:
        pass
    
    # If it is the friend requester sending further messages, then reject
    try:
        friend_request = FriendRequest.objects().get(requester=sender, requestee=receiver)
        if friend_request.expired:
            # last request expired, reactivate it
            friend_request.modify(expired=False)

            thread = threading.Thread(target=create_friend_request_expiry_job, args=(f"{sender_uid}@uwaterloo.ca", f"{receiver_uid}@uwaterloo.ca", current_app.config['COMETCHAT_APP_ID'], current_app.config["COMETCHAT_API_KEY"]))
            thread.start()

            return {}
        elif not friend_request.approved:
            return {"action": "do_not_propagate"}
        return {}  # friend request is already approved
    except FriendRequest.DoesNotExist:
        pass
    
    # The sender is sending the first message to the receiver, then add a friend request and permit
    friend_request = FriendRequest(requester=sender, requestee=receiver)
    friend_request.validate()
    friend_request.save()

    thread = threading.Thread(target=create_friend_request_expiry_job, args=(f"{sender_uid}@uwaterloo.ca", f"{receiver_uid}@uwaterloo.ca", current_app.config['COMETCHAT_APP_ID'], current_app.config["COMETCHAT_API_KEY"]))
    thread.start()

    return {}