# Credit to Liam Middlebrook and Ram Zallan
# https://github.com/liam-middlebrook/gallery


from functools import wraps

from flask import session

from .ldap import ldap_is_financial


def user_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uuid = str(session["userinfo"].get("sub", ""))
        uid = str(session["userinfo"].get("preferred_username", ""))
        is_financial = ldap_is_financial(uid)

        auth_dict = {
            "uuid": uuid,
            "uid": uid,
            "is_financial": is_financial
        }
        kwargs["auth_dict"] = auth_dict

        return func(*args, **kwargs)

    return wrapped_function


def financial_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uuid = str(session["userinfo"].get("sub", ""))
        uid = str(session["userinfo"].get("preferred_username", ""))
        is_financial = ldap_is_financial(uid)

        auth_dict = {
            "uuid": uuid,
            "uid": uid,
            "is_financial": is_financial
        }
        kwargs["auth_dict"] = auth_dict

        if is_financial:
            return func(*args, **kwargs)

    return wrapped_function
