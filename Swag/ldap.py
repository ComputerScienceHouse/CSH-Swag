from functools import lru_cache

from Swag import _ldap


@lru_cache(maxsize=1024)
def ldap_is_financial(uid):
    financial = _ldap.get_directorship_heads("financial")
    return financial[0].get("uid")[0] == uid


@lru_cache(maxsize=1024)
def ldap_is_rtp(uid):
    return _ldap.ldap_is_member_of_group(_ldap.get_member(uid, uid=True), 'rtp')


@lru_cache(maxsize=1024)
def get_current_students():
    return [{"uid": member.get("uid")[0], "cn": member.get("cn")[0]} for member in
            _ldap.get_group('current_student').get_members()]


@lru_cache(maxsize=2048)
def get_all_members():
    return [{"uid": member.get("uid")[0], "cn": member.get("cn")[0]} for member in
            _ldap.get_group('member').get_members()]
