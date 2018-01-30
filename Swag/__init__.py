import os
import requests
import subprocess

import flask_migrate
# from csh_ldap import CSHLDAP
from flask import Flask, render_template, jsonify, request
# from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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

# auth = OIDCAuthentication(app,
#                           issuer=app.config["OIDC_ISSUER"],
#                           client_registration_info=app.config["OIDC_CLIENT_CONFIG"])

# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Import db models after instantiating db object
from Swag.models import Swag, Item, Stock, Receipt, Review

# Create CSHLDAP connection
# ldap = CSHLDAP(app.config["LDAP_BIND_DN"],
#                app.config["LDAP_BIND_PW"])

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()


@app.route("/", methods=["GET"])
def home(auth_dict=None):
    db.create_all()
    items = Item.query.order_by(func.rand()).all()
    # TODO: Get swag items where all items have stock > 0
    return render_template("index.html", auth_dict=auth_dict, items=items)


@app.route('/category/<category_name>', methods=['GET'])
def category(category_name, auth_dict=None):
    items = Item.query.all()
    return render_template("category.html", auth_dict=auth_dict, category_name=category_name, items=items)


@app.route('/item/<item_id>', methods=['GET'])
def item(item_id, auth_dict=None):
    item = Item.query.get(item_id)
    stock = Stock.query.filter_by(item_id=item_id).order_by("size ASC")
    reviews = Review.query.filter_by(item_id=item_id)
    # TODO: Check if user has purchased item before

    return render_template("item.html", auth_dict=auth_dict, item_id=item_id, item=item, stock=stock, reviews=reviews)


@app.route("/manage", methods=["GET"])
def financial(auth_dict=None):
    db.create_all()
    items = Item.query.all()
    stock = Stock.query.all()
    return render_template("manage/dashboard.html", auth_dict=auth_dict, items=items, stock=stock)


@app.route("/swag", methods=["GET"])
def swag():
    return jsonify(data=[i.serialize for i in Swag.query.all()])


@app.route("/update/swag", methods=["POST"])
def update_swag():
    data = request.form
    return jsonify(data)


@app.route("/items", methods=["GET"])
def items():
    return jsonify(data=[i.serialize for i in Item.query.all()])


@app.route("/stock/<item_id>", methods=["GET"])
def stock(item_id):
    return jsonify(data=[i.serialize for i in Stock.query.filter_by(item_id=item_id)])


@app.route("/receipts", methods=["GET"])
def receipts():
    return jsonify(data=[i.serialize for i in Receipt.query.all()])
