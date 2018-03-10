from flask import request, jsonify

from Swag import app, auth, financial_auth, Swag, db, Item, Stock


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
