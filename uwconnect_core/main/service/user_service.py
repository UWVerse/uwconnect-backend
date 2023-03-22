from flask import session
from werkzeug.exceptions import Forbidden
import requests
from flask import current_app


def set_session(key, val):
    session[key] = val


def get_session(key):
    return session[key]


def pop_session(key):
    session.pop(key, None)


def check_login(func):
    def wrapper(*args, **kwargs):
        try:
            get_session("email")
        except:
            # return redirect(app.config['FRONTEND_DOMAIN'] + '/')
            raise Forbidden("client not logged in")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def cometchat_create_user(uid, username):
    # url = f"https://{current_app.config['COMETCHAT_APP_ID']}.api-us.cometchat.io/v3/users"

    # payload = {
    #             "uid": uid,
    #             "name": username
    #         }
    # headers = {
    #     "accept": "application/json",
    #     "content-type": "application/json",
    #     "apikey": current_app.config["COMETCHAT_API_KEY"]
    # }

    # requests.post(url, json=payload, headers=headers)
    return 
