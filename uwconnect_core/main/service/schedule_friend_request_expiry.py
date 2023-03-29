import schedule
import time
from uwconnect_core.main.model.friend import FriendRequest
from uwconnect_core.main.model.user import User


def create_friend_request_expiry_job(sender_email, receiver_email):
    def job(sender_email, receiver_email):
        sender = User.objects().get(email=sender_email)
        receiver = User.objects().get(email=receiver_email)
        friend_request = FriendRequest.objects().get(requester=receiver, requestee=sender)

        if friend_request.approved:
            return
        friend_request.modify(expired=True)


    schedule.run_in(24*60*60, job, sender_email, receiver_email)




schedule.run_in(10, job) # Job will run once after 10 seconds

while True:
    schedule.run_pending()
    time.sleep(1)