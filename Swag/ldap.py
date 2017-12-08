from Swag import ldap


def ldap_is_financial(uid):
    financial = ldap.get_directorship_heads("Financial Director")
    print(uid + " : " + financial)
