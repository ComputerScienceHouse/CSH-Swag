from Swag import ldap


def ldap_is_financial(uid):
    financial = ldap.get_directorship_heads("Financial")
    return financial[0].get("uid")[0] == uid


def get_active_members():
    active_members = [{"uid": member.get("uid")[0], "cn": member.get("cn")[0]} for member in
                      ldap.get_group("cron").get_members()]
    return active_members
