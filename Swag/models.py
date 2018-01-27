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


class Swag(db.Model):
    __tablename__ = "swag"
    swag_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = db.Column(db.VARCHAR(45), nullable=False)
    description = db.Column(db.VARCHAR(255))
    category = db.Column(db.VARCHAR(45), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'swag_id': self.swag_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
        }


class Item(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey("swag.swag_id"), nullable=False)
    product = db.relationship(Swag, backref=db.backref("swag", uselist=False))
    color = db.Column(db.VARCHAR(45), nullable=False)
    image = db.Column(db.VARCHAR(255), nullable=True)

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
    item = db.relationship(Item, backref=db.backref("item", uselist=False))
    size = db.Column(db.Enum(SizeOptions), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)

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
    datetime = db.Column(db.DateTime, nullable=False)
    purchased = db.relationship(Stock, backref=db.backref("Stock", uselist=False))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    member_uid = db.Column(db.VARCHAR(75), nullable=True)
    discount_id = db.Column(db.Integer, nullable=True)
    shipping = db.Column(db.Boolean, nullable=False, default=False)
    shipping_cost = db.Column(db.Integer, nullable=True)
    method = db.Column(db.Enum(PaymentMethod), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'receipt_id': self.receipt_id,
            'datetime': self.datetime.strftime('%m/%d/%Y'),
            'purchased': self.purchased.serialize,
            'quantity': self.quantity,
            'member_uid': self.member_uid,
            'method': self.method.name,
        }
