import os

import flask_migrate
import requests
from csh_ldap import CSHLDAP
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

auth = OIDCAuthentication(app, issuer=app.config["OIDC_ISSUER"],
                          client_registration_info=app.config["OIDC_CLIENT_CONFIG"])

# Create CSHLDAP connection
_ldap = CSHLDAP(app.config["LDAP_BIND_DN"],
               app.config["LDAP_BIND_PW"])

# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Import db and ldap models after instantiating db object
# pylint: disable=wrong-import-position
from .models import Swag, Item, Stock, Receipt, Review
from .ldap import get_active_members
from .utils import user_auth, financial_auth

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()


@app.route('/favicon.ico')
def _favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=["GET"])
@auth.oidc_auth
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


@app.route('/category/<category_name>', methods=['GET'])
@auth.oidc_auth
@user_auth
def _category(category_name, auth_dict=None):
    items = Item.query.all()
    return render_template("category.html", auth_dict=auth_dict, category_name=category_name, items=items)


@app.route('/item/<item_id>', methods=['GET'])
@auth.oidc_auth
@user_auth
def _item(item_id, auth_dict=None):
    item = Item.query.get(item_id)
    stock = Stock.query.filter_by(item_id=item_id).order_by("size ASC")
    reviews = Review.query.filter_by(item_id=item_id)

    # Check if the item has ever been purchased by that user
    receipts = [Receipt.query.filter_by(member_uid=auth_dict['uid'], stock_id=stock_item.stock_id).first() for
                stock_item in stock]
    receipts = list(filter(None.__ne__, receipts))
    current_review = Review.query.filter_by(member_uid=auth_dict['uid']).first()

    return render_template("item.html", auth_dict=auth_dict, item_id=item_id, item=item, stock=stock, reviews=reviews,
                           receipts=receipts, current_review=current_review)


@app.route("/manage", methods=["GET"])
@auth.oidc_auth
@financial_auth
def _financial(auth_dict=None):
    if auth_dict["is_financial"]:
        db.create_all()
        venmo = 0
        items = Item.query.all()
        stock = Stock.query.all()
        all_stock = Stock.query.all()
        active_members = get_active_members()
        for i in Receipt.query.filter_by(method="Venmo"):
            venmo += i.purchased.item.product.price * i.quantity
        return render_template("manage/dashboard.html", auth_dict=auth_dict, items=items, stock=stock, venmo=venmo,
                               active_members=active_members, all_stock=all_stock)
    return 403


@app.route("/swag", methods=["GET"])
@auth.oidc_auth
@financial_auth
def _swag(auth_dict=None):
    if auth_dict["is_financial"]:
        return jsonify(data=[i.serialize for i in Swag.query.all()])
    return 403


@app.route("/update/swag", methods=["POST"])
@auth.oidc_auth
@financial_auth
def _update_swag(auth_dict=None):
    if auth_dict["is_financial"]:
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
@financial_auth
def _update_item(auth_dict=None):
    if auth_dict["is_financial"]:
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
@financial_auth
def _update_stock(auth_dict=None):
    if auth_dict["is_financial"]:
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
@financial_auth
def _new_transaction(auth_dict=None):
    if auth_dict["is_financial"]:
        data = request.form
        transaction = Receipt(data['transaction-item-id'], data['receipt-member'],
                              data['payment-method'], data['item-quantity'])
        stock_item = Stock.query.filter_by(stock_id=data['transaction-item-id'])
        stock_item.stock -= 1
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.serialize)
    return 403


@app.route("/new/review", methods=["PUT"])
@auth.oidc_auth
@user_auth
def _new_review(auth_dict=None):
    data = request.form
    review = Review(auth_dict['uid'], data['item-id'], data['rating'], data['review-text'])
    db.session.add(review)
    db.session.commit()
    return 205


@app.route("/items", methods=["GET"])
@auth.oidc_auth
@financial_auth
def _items(auth_dict=None):
    if auth_dict["is_financial"]:
        return jsonify(data=[i.serialize for i in Item.query.all()])
    return 403


@app.route("/stock/<item_id>", methods=["GET"])
@auth.oidc_auth
@financial_auth
def _stock(item_id, auth_dict=None):
    if auth_dict["is_financial"]:
        return jsonify(data=[i.serialize for i in Stock.query.filter_by(item_id=item_id)])
    return 403


@app.route("/receipts", methods=["GET"])
@auth.oidc_auth
@financial_auth
def _receipts(auth_dict=None):
    if auth_dict["is_financial"]:
        return jsonify(data=[i.serialize for i in Receipt.query.all()])
    return 403
