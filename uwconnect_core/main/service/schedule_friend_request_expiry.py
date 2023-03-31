from time import sleep

from uwconnect_core.main.model.friend import FriendRequest
from uwconnect_core.main.model.user import User
from uwconnect_core.main.service.cometchat_api import reset_conversation


def create_friend_request_expiry_job(sender_email, receiver_email, COMETCHAT_APP_ID, COMETCHAT_API_KEY):
    sleep(10)

    sender = User.objects().get(email=sender_email)
    receiver = User.objects().get(email=receiver_email)
    try:
        friend_request = FriendRequest.objects().get(requester=sender, requestee=receiver)
        if friend_request.approved:
            return
        friend_request.modify(expired=True)

        reset_conversation(sender_email.split('@')[0], receiver_email.split('@')[0], COMETCHAT_APP_ID, COMETCHAT_API_KEY)
        
    except FriendRequest.DoesNotExist:
        pass



