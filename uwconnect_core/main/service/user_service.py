from flask import session
from werkzeug.exceptions import Forbidden


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