import os

import flask_migrate
import requests
from csh_ldap import CSHLDAP
from flask import Flask, render_template, jsonify, redirect, send_from_directory
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

APP_CONFIG = ProviderConfiguration(issuer=app.config["OIDC_ISSUER"],
                          client_metadata=ClientMetadata(app.config["OIDC_CLIENT_CONFIG"]['client_id'],
                                                            app.config["OIDC_CLIENT_CONFIG"]['client_secret']))

auth = OIDCAuthentication({'app': APP_CONFIG}, app)

# Create CSHLDAP connection
_ldap = CSHLDAP(app.config["LDAP_BIND_DN"],
                app.config["LDAP_BIND_PW"])

# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Import db and ldap models after instantiating db object
# pylint: disable=wrong-import-position
from .models import Swag, Item, Stock, Receipt, Review, CashFlow
from .ldap import get_all_members
from .utils import user_auth, authorized_auth, current_balances

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()

# Import routes
from .routes import update, new


@app.route('/favicon.ico')
def _favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=["GET"])
@auth.oidc_auth('app')
@user_auth
def _home(auth_dict=None):
    db.create_all()
    items = Item.query.order_by(Item.product_id).all()
    # TODO: Get swag items where all items have stock > 0
    return render_template("index.html", auth_dict=auth_dict, items=items)


@app.route("/logout")
@auth.oidc_logout
def _logout():
    return redirect("/", 302)


@app.route('/item/<item_id>', methods=['GET'])
@auth.oidc_auth('app')
@user_auth
def _item(item_id, auth_dict=None):
    item = Item.query.get(item_id)
    stock = Stock.query.filter_by(item_id=item_id).order_by("size ASC")
    reviews = Review.query.filter_by(item_id=item_id)

    # Check if the item has ever been purchased by that user
    receipts = [Receipt.query.filter_by(member_uid=auth_dict['uid'], stock_id=stock_item.stock_id).first() for
                stock_item in stock]
    receipts = list(filter(None.__ne__, receipts))
    current_review = Review.query.filter_by(member_uid=auth_dict['uid'], item_id=item_id).first()

    return render_template("item.html", auth_dict=auth_dict, item_id=item_id, item=item, stock=stock, reviews=reviews,
                           receipts=receipts, current_review=current_review)


@app.route('/history', methods=['GET'])
@auth.oidc_auth('app')
@user_auth
def _history(auth_dict=None):
    return render_template("history.html", auth_dict=auth_dict)


@app.route("/admin/inventory", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _inventory(auth_dict=None):
    if auth_dict["is_authorized"]:
        db.create_all()
        return render_template("admin/inventory.html", auth_dict=auth_dict)
    return 403


@app.route("/admin/cashflow", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _cashflow(auth_dict=None):
    if auth_dict["is_authorized"]:
        db.create_all()
        return render_template("admin/cashflow.html", auth_dict=auth_dict)
    return 403


@app.route("/admin/transactions", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _transactions(auth_dict=None):
    if auth_dict["is_authorized"]:
        db.create_all()
        all_members = get_all_members()
        balances = current_balances()
        all_stock = Stock.query.all()
        return render_template("admin/transactions.html", auth_dict=auth_dict, balances=balances,
                               active_members=all_members, all_stock=all_stock)
    return 403


@app.route("/swag", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _swag(auth_dict=None):
    if auth_dict["is_authorized"]:
        return jsonify(data=[i.serialize for i in Swag.query.all()])
    return 403


@app.route("/items", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _items(auth_dict=None):
    if auth_dict["is_authorized"]:
        return jsonify(data=[i.serialize for i in Item.query.all()])
    return 403


@app.route("/stock/<item_id>", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _stock(item_id, auth_dict=None):
    if auth_dict["is_authorized"]:
        return jsonify(data=[i.serialize for i in Stock.query.filter_by(item_id=item_id)])
    return 403


@app.route("/receipts", methods=["GET"])
@auth.oidc_auth('app')
@user_auth
def _receipts(auth_dict=None):
    return jsonify(data=[i.serialize for i in Receipt.query.filter_by(member_uid=auth_dict['uid']).all()])


@app.route("/receipts/all", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _receipts_all(auth_dict=None):
    if auth_dict["is_authorized"]:
        return jsonify(data=[i.serialize for i in Receipt.query.all()])
    return 403


@app.route("/cashflow/all", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _cashflow_all(auth_dict=None):
    if auth_dict["is_authorized"]:
        return jsonify(data=[i.serialize for i in CashFlow.query.all()])
    return 403


@app.route("/methods", methods=["GET"])
@auth.oidc_auth('app')
@user_auth
def _methods(auth_dict=None):
    total = {
        "Cash": 0,
        "Venmo": 0,
        "Check": 0
    }
    receipts = Receipt.query.filter_by(member_uid=auth_dict['uid']).all()
    for i in receipts:
        total[i.method.name] += i.quantity
    return jsonify(total)


@app.route("/methods/all", methods=["GET"])
@auth.oidc_auth('app')
@authorized_auth
def _methods_all(auth_dict=None):
    if auth_dict["is_authorized"]:
        total = {
            "Cash": 0,
            "Venmo": 0,
            "Check": 0
        }
        receipts = Receipt.query.all()
        for i in receipts:
            total[i.method.name] += i.quantity
        return jsonify(total)
    return 403
