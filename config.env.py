import secrets
from os import environ as env

# Flask config
DEBUG = True
IP = env.get('SWAG_IP', 'localhost')
PORT = env.get('SWAG_PORT', 3000)
SERVER_NAME = env.get('SWAG_SERVER_NAME', 'localhost:3000')

# DB Info
SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI', '<your URI here>')

# Openshift secret
SECRET_KEY = env.get("SECRET_KEY", default='<your secret key here>'.join(secrets.token_hex(16)))

# OpenID Connect SSO config
OIDC_ISSUER = env.get('SWAG_OIDC_ISSUER', 'https://sso.csh.rit.edu/auth/realms/csh')
OIDC_CLIENT_CONFIG = {
    'client_id': env.get('SWAG_OIDC_CLIENT_ID', 'swag'),
    'client_secret': env.get('SWAG_OIDC_CLIENT_SECRET', '<your secret here>'),
    'post_logout_redirect_uris': [env.get('SWAG_OIDC_LOGOUT_REDIRECT_URI', 'https://swag.csh.rit.edu/logout')]
}

# CSH_LDAP credentials
LDAP_BIND_DN = env.get("LDAP_BIND_DN", default="<your dn here>cn=swag,ou=Apps,dc=csh,dc=rit,dc=edu")
LDAP_BIND_PW = env.get("LDAP_BIND_PW", default="<your pw here>")
