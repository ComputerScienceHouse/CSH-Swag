import os
import subprocess

import flask_migrate
import requests
from csh_ldap import CSHLDAP
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_optimize import FlaskOptimize
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy

from Swag.utils import swag_auth

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

flask_optimize = FlaskOptimize()

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

# Create CSHLDAP connection
ldap = CSHLDAP(app.config["LDAP_BIND_DN"],
               app.config["LDAP_BIND_PW"])

# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Import db and ldap models after instantiating db object
from .models import Swag, Item, Stock, Receipt, Review
from .ldap import ldap_is_financial, get_active_members

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=["GET"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize()
def home(auth_dict=None):
    db.create_all()
    items = Item.query.all()
    # TODO: Get swag items where all items have stock > 0
    return render_template("index.html", auth_dict=auth_dict, items=items)


@app.route("/logout")
@auth.oidc_logout
@swag_auth
def logout():
    return redirect("/", 302)


@app.route('/category/<category_name>', methods=['GET'])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize()
def category(category_name, auth_dict=None):
    items = Item.query.all()
    return render_template("category.html", auth_dict=auth_dict, category_name=category_name, items=items)


@app.route('/item/<item_id>', methods=['GET'])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize()
def item(item_id, auth_dict=None):
    item = Item.query.get(item_id)
    stock = Stock.query.filter_by(item_id=item_id).order_by("size ASC")
    reviews = Review.query.filter_by(item_id=item_id)

    # Check if the item has ever been purchased by that user
    receipts = [Receipt.query.filter_by(member_uid=auth_dict['uid'], stock_id=stock_item.stock_id).first() for
                stock_item in stock]
    receipts = list(filter(None.__ne__, receipts))

    return render_template("item.html", auth_dict=auth_dict, item_id=item_id, item=item, stock=stock, reviews=reviews,
                           receipts=receipts)


@app.route("/manage", methods=["GET"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize()
def financial(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        db.create_all()
        venmo = 0
        items = Item.query.all()
        stock = Stock.query.all()
        active_members = get_active_members()
        for i in Receipt.query.filter_by(method="Venmo"):
            venmo += i.purchased.item.product.price * i.quantity
        return render_template("manage/dashboard.html", auth_dict=auth_dict, items=items, stock=stock, venmo=venmo,
                               active_members=active_members)
    return 403


@app.route("/swag", methods=["GET"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def swag(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        return jsonify(data=[i.serialize for i in Swag.query.all()])
    return 403


@app.route("/update/swag", methods=["POST"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def update_swag(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        data = request.form
        swag = Swag.query.get(data['product-id'])
        swag.name = data['product-name']
        swag.description = data['description-text']
        swag.price = data['price-value']
        swag.category = data['category-name']
        db.session.commit()
        return jsonify(swag.serialize)
    return 403


@app.route("/update/item", methods=["POST"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def update_item(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        data = request.form
        item = Item.query.get(data['item-id'])
        item.color = data['color-text']
        item.product_id = data['product-id']
        item.image = data['image-url']
        db.session.commit()
        return jsonify(data)
    return 403


@app.route("/update/stock", methods=["POST"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def update_stock(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        data = request.form
        for value in data:
            stock = Stock.query.get(value)
            if stock is not None:
                stock.stock = data.get(value)
        db.session.commit()
        return jsonify(data)
    return 403


@app.route("/new/transaction", methods=["PUT"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def new_transaction(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        data = request.form
        transaction = Receipt(data['transaction-item-id'], data['receipt-member'],
                              data['payment-method'], data['item-quantity'])
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.serialize)
    return 403


@app.route("/new/review", methods=["PUT"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def new_review(auth_dict=None):
    data = request.form
    return jsonify(data)


@app.route("/items", methods=["GET"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def items(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        return jsonify(data=[i.serialize for i in Item.query.all()])
    return 403


@app.route("/stock/<item_id>", methods=["GET"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def stock(item_id, auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        return jsonify(data=[i.serialize for i in Stock.query.filter_by(item_id=item_id)])
    return 403


@app.route("/receipts", methods=["GET"])
@auth.oidc_auth
@swag_auth
@flask_optimize.optimize('json')
def receipts(auth_dict=None):
    if ldap_is_financial(auth_dict["uid"]):
        return jsonify(data=[i.serialize for i in Receipt.query.all()])
    return 403
