import enum

from Swag import db


class Category(enum.Enum):
    Shirts = 1
    Sweatshirts = 2
    Glassware = 3
    Stickers = 4
    Misc = 5


class ShirtSize(enum.Enum):
    S = 1
    M = 2
    L = 3
    XL = 4
    XXL = 5
    XXXL = 6


class Swag(db.Model):
    __tablename__ = "swag"
    swag_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(45), nullable=False)
    description = db.Column(db.VARCHAR(255))
    category = db.Column(db.VARCHAR(45), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Item(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("swag.swag_id"), nullable=False)
    product = db.relationship("Swag", backref=db.backref("swag", uselist=False))
    color = db.Column(db.VARCHAR(45), nullable=False)
    image = db.Column(db.VARCHAR(255), nullable=True)


class ItemSize(db.Model):
    __tablename__ = "item_sizes"
    size_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    size = db.Column(db.Enum(ShirtSize), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
