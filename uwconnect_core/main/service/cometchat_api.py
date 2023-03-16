import requests
from uwconnect_core.main import app

def get_friends(uid, friend_uid):
    url = f"https://{app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users/{uid}/friends"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": app.config["COMETCHAT_API_KEY"]
    }
    if friend_uid:
        url += f"?searchKey={friend_uid}"
    return requests.get(url, headers=headers).json().get("data")

def add_friends(uid, friend_uid):
    url = f"https://{app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users/{uid}/friends"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": app.config["COMETCHAT_API_KEY"]
    }
    payload = {"accepted": [friend_uid]}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return True
    raise Exception(f"failed to add friend on cometchat server: {response.text}")
