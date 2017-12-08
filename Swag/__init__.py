import hashlib, os, flask_migrate, requests, subprocess, random, json
from flask import Flask, render_template, request, jsonify, redirect
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from csh_ldap import CSHLDAP

from Swag.ldap import ldap_is_financial
from Swag.utils import swag_auth

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

app.config["GIT_REVISION"] = subprocess.check_output(['git',
                                                      'rev-parse',
                                                      '--short',
                                                      'HEAD']).decode('utf-8').rstrip()

auth = OIDCAuthentication(app,
                          issuer=app.config["OIDC_ISSUER"],
                          client_registration_info=app.config["OIDC_CLIENT_CONFIG"])

# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Create CSHLDAP connection
ldap = CSHLDAP(app.config["LDAP_BIND_DN"],
               app.config["LDAP_BIND_PW"])


# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()


@app.route("/")
@auth.oidc_auth
@swag_auth
def home(auth_dict=None):
    return ldap_is_financial(auth_dict["uid"])
