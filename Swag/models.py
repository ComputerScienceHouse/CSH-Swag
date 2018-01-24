from Swag import db


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
    product = db.Column(db.Integer, db.ForeignKey("swag.swag_id"), nullable=False)
    color = db.Column(db.VARCHAR(45), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)


class ItemImage(db.Model):
    __tablename__ = "itemImage"
    image_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    image_path = db.Column(db.VARCHAR(255), nullable=False)
