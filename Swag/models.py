import datetime
import enum

from Swag import db


class Category(enum.Enum):
    Shirts = 1
    Sweatshirts = 2
    Glassware = 3
    Stickers = 4
    Misc = 5


class PaymentMethod(enum.Enum):
    Cash = 1
    Check = 2
    Venmo = 3
    Card = 4
    Online = 5


class SizeOptions(enum.Enum):
    Standard = 0
    S = 1
    M = 2
    L = 3
    XL = 4
    XXL = 5
    XXXL = 6
    Square = 7
    Rounded = 8


class Swag(db.Model):
    __tablename__ = "swag"
    swag_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = db.Column(db.VARCHAR(45), nullable=False)
    description = db.Column(db.VARCHAR(255))
    category = db.Column(db.VARCHAR(45), nullable=False)
    price = db.Column(db.DECIMAL(25, 2), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'swag_id': self.swag_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': str(self.price),
        }


class Item(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey("swag.swag_id"), nullable=False)
    color = db.Column(db.VARCHAR(45), nullable=False)
    image = db.Column(db.VARCHAR(255), nullable=True)

    product = db.relationship(Swag, backref=db.backref("swag", uselist=False))

    @property
    def stock(self):
        item_stock = Stock.query.filter_by(item_id=self.item_id)
        return sum(i.stock for i in item_stock)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        item_stock = Stock.query.filter_by(item_id=self.item_id)
        return {
            'item_id': self.item_id,
            'product': self.product.serialize,
            'color': self.color,
            'image': self.image,
            'stock': self.stock,
            'sizes': [i.serialize for i in item_stock]
        }

    @property
    def serialize_single(self):
        """Return object data in easily serializeable format"""
        item_stock = Stock.query.filter_by(item_id=self.item_id)
        stock = sum(i.stock for i in item_stock)
        return {
            'item_id': self.item_id,
            'product': self.product.serialize,
            'color': self.color,
            'image': self.image,
            'stock': stock,
        }


class Stock(db.Model):
    __tablename__ = "stock"
    stock_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    size = db.Column(db.Enum(SizeOptions), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)

    item = db.relationship(Item, backref=db.backref("item", uselist=False))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'stock_id': self.stock_id,
            'size': self.size.name,
            'stock': self.stock,
            'item': self.item.serialize_single,
        }


class Receipt(db.Model):
    __tablename__ = "receipts"
    receipt_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.stock_id"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    member_uid = db.Column(db.VARCHAR(75), nullable=True)
    method = db.Column(db.Enum(PaymentMethod), nullable=True)

    purchased = db.relationship(Stock, backref=db.backref("Stock", uselist=False))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'receipt_id': self.receipt_id,
            'datetime': self.datetime.strftime('%m/%d/%Y'),
            'purchased': self.purchased.serialize,
            'cost': self.quantity * float(self.purchased.item.product.price),
            'quantity': self.quantity,
            'member_uid': self.member_uid,
            'method': self.method.name,
        }

    def __init__(self, item_id, member_uid, method, quantity):
        self.stock_id = item_id
        self.member_uid = member_uid
        self.method = method
        self.quantity = quantity


class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    member_uid = db.Column(db.VARCHAR(75), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    review_score = db.Column(db.Float)
    review_text = db.Column(db.Text)

    def __init__(self, member_uid, item_id, review_score, review_text):
        self.member_uid = member_uid
        self.item_id = item_id
        self.review_score = review_score
        self.review_text = review_text
