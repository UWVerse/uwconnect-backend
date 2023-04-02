import requests
from flask import current_app

def get_friends(uid, friend_uid=None):
    url = f"https://{current_app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users/{uid}/friends"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": current_app.config["COMETCHAT_API_KEY"]
    }
    if friend_uid:
        url += f"?searchKey={friend_uid}"
    uids = requests.get(url, headers=headers).json().get("data")
    return uids

def add_friends(uid, friend_uid):
    url = f"https://{current_app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users/{uid}/friends"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": current_app.config["COMETCHAT_API_KEY"]
    }
    payload = {"accepted": [friend_uid]}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return True
    raise Exception(f"failed to add friend on cometchat server: {response.text}")

def remove_friends(uid, friend_uid):
    url = f"https://{current_app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users/{uid}/friends"
    payload = {"friends": [friend_uid]}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": current_app.config["COMETCHAT_API_KEY"]
    }
    response = requests.delete(url, json=payload, headers=headers)
    if response.status_code == 200:
        return True
    raise Exception(f"failed to remove friend on cometchat server: {response.text}")

def add_user(uid, username):
    url = f"https://{current_app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users"

    payload = {
                "uid": uid,
                "name": username
            }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": current_app.config["COMETCHAT_API_KEY"]
    }

    requests.post(url, json=payload, headers=headers)

def remove_user(uid):
    url = f"https://{current_app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users/{uid}"

    payload = {"permanent": "false"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": current_app.config["COMETCHAT_API_KEY"]
    }

    requests.delete(url, json=payload, headers=headers)
