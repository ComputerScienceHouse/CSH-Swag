# Credit to Liam Middlebrook and Ram Zallan
# https://github.com/liam-middlebrook/gallery


from functools import wraps

from flask import session

from Swag import Receipt
from Swag.models import CashFlow
from .ldap import ldap_is_financial, ldap_is_rtp


def user_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uuid = str(session["userinfo"].get("sub", ""))
        uid = str(session["userinfo"].get("preferred_username", ""))
        is_financial = ldap_is_financial(uid)
        is_rtp = ldap_is_rtp(uid)

        auth_dict = {
            "uuid": uuid,
            "uid": uid,
            "is_financial": is_financial,
            "is_rtp": is_rtp
        }
        kwargs["auth_dict"] = auth_dict

        return func(*args, **kwargs)

    return wrapped_function


def authorized_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uuid = str(session["userinfo"].get("sub", ""))
        uid = str(session["userinfo"].get("preferred_username", ""))
        is_financial = ldap_is_financial(uid)
        is_rtp = ldap_is_rtp(uid)

        auth_dict = {
            "uuid": uuid,
            "uid": uid,
            "is_financial": is_financial,
            "is_rtp": is_rtp,
            "is_authorized": is_financial or is_rtp,
        }
        kwargs["auth_dict"] = auth_dict

        if is_financial or is_rtp:
            return func(*args, **kwargs)
        return None

    return wrapped_function


def current_balances():
    receipts = Receipt.query.all()
    cash_flow = CashFlow.query.all()
    balances = {
        "Cash": 0,
        "Venmo": 0,
        "Check": 0
    }
    for receipt in receipts:
        balances[receipt.method.name] += receipt.purchased.item.product.price * receipt.quantity

    for flow in cash_flow:
        if flow.account_from:
            balances[flow.account_from.name] -= flow.amount
        if flow.account_to:
            balances[flow.account_to.name] += flow.amount

    return balances
