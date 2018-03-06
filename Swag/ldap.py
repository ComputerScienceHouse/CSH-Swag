from Swag import ldap


def ldap_is_financial(uid):
    financial = ldap.get_directorship_heads("Financial")
    return financial[0].get("uid")[0] == uid
