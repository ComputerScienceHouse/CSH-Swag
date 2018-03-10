from flask import request, jsonify

from Swag import app, auth, financial_auth, db, user_auth
from Swag.models import Receipt, Stock, Review


@app.route("/new/transaction", methods=["PUT"])
@auth.oidc_auth
@financial_auth
def _new_transaction(auth_dict=None):
    if auth_dict["is_financial"]:
        data = request.form
        transaction = Receipt(data['transaction-item-id'], data['receipt-member'],
                              data['payment-method'], data['item-quantity'])
        stock_item = Stock.query.filter_by(stock_id=data['transaction-item-id']).first()
        stock_item.stock -= int(data['item-quantity'])
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.serialize)
    return 403


@app.route("/new/review", methods=["PUT"])
@auth.oidc_auth
@user_auth
def _new_review(auth_dict=None):
    data = request.form
    existing_review = Review.query.filter_by(member_uid=auth_dict['uid'], item_id=data['item-id']).first()
    if existing_review is None:
        review = Review(auth_dict['uid'], data['item-id'], data['rating'], data['review-text'])
        db.session.add(review)
        db.session.commit()
        return 205
    return 400
