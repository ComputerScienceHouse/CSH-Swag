import os
import requests
import subprocess

import flask_migrate
from flask import Flask, render_template, jsonify, request, redirect
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
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

auth = OIDCAuthentication(app, issuer=app.config["OIDC_ISSUER"],
                          client_registration_info=app.config["OIDC_CLIENT_CONFIG"])

# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Import db models after instantiating db object
from Swag.models import Swag, Item, Stock, Receipt, Review

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()


@app.route("/", methods=["GET"])
@auth.oidc_auth
def home(auth_dict=None):
    db.create_all()
    items = Item.query.all()
    # TODO: Get swag items where all items have stock > 0
    return render_template("index.html", auth_dict=auth_dict, items=items)


@app.route("/logout")
@auth.oidc_logout
def logout():
    return redirect("/", 302)


@app.route('/category/<category_name>', methods=['GET'])
@auth.oidc_auth
def category(category_name, auth_dict=None):
    items = Item.query.all()
    return render_template("category.html", auth_dict=auth_dict, category_name=category_name, items=items)


@app.route('/item/<item_id>', methods=['GET'])
@auth.oidc_auth
def item(item_id, auth_dict=None):
    item = Item.query.get(item_id)
    stock = Stock.query.filter_by(item_id=item_id).order_by("size ASC")
    reviews = Review.query.filter_by(item_id=item_id)
    # TODO: Check if user has purchased item before

    return render_template("item.html", auth_dict=auth_dict, item_id=item_id, item=item, stock=stock, reviews=reviews)


@app.route("/manage", methods=["GET"])
@auth.oidc_auth
@swag_auth
def financial(auth_dict=None):
    db.create_all()
    items = Item.query.all()
    stock = Stock.query.all()
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return render_template("manage/dashboard.html", auth_dict=auth_dict, items=items, stock=stock)


@app.route("/swag", methods=["GET"])
@auth.oidc_auth
@swag_auth
def swag(auth_dict=None):
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return jsonify(data=[i.serialize for i in Swag.query.all()])


@app.route("/update/swag", methods=["POST"])
@auth.oidc_auth
@swag_auth
def update_swag(auth_dict=None):
    data = request.form
    swag = Swag.query.get(data['product-id'])
    swag.name = data['product-name']
    swag.description = data['description-text']
    swag.price = data['price-value']
    swag.category = data['category-name']
    db.session.commit()
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return jsonify(swag.serialize)


@app.route("/update/item", methods=["POST"])
@auth.oidc_auth
@swag_auth
def update_item(auth_dict=None):
    data = request.form
    item = Item.query.get(data['item-id'])
    item.color = data['color-text']
    item.product_id = data['product-id']
    item.image = data['image-url']
    db.session.commit()
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return jsonify(data)


@app.route("/new/transaction", methods=["PUT"])
@auth.oidc_auth
@swag_auth
def new_transaction(auth_dict=None):
    data = request.form
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return jsonify(data)


@app.route("/items", methods=["GET"])
@auth.oidc_auth
@swag_auth
def items(auth_dict=None):
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return jsonify(data=[i.serialize for i in Item.query.all()])


@app.route("/stock/<item_id>", methods=["GET"])
@auth.oidc_auth
@swag_auth
def stock(item_id, auth_dict=None):
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return jsonify(data=[i.serialize for i in Stock.query.filter_by(item_id=item_id)])


@app.route("/receipts", methods=["GET"])
@auth.oidc_auth
@swag_auth
def receipts(auth_dict=None):
    # TODO: Check to make sure financial
    if auth_dict["uid"] == "matted":
        return jsonify(data=[i.serialize for i in Receipt.query.all()])
