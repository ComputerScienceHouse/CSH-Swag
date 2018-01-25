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
    product_id = db.Column(db.Integer, db.ForeignKey("swag.swag_id"), nullable=False)
    product = db.relationship("Swag", backref=db.backref("swag", uselist=False))
    color = db.Column(db.VARCHAR(45), nullable=False)
    image = db.Column(db.VARCHAR(255), nullable=True)


class itemSize(db.Model):
    __tablename__ = "item_sizes"
    size_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"), nullable=False)
    item = db.relationship("Item", backref=db.backref("items", useList=False))
    size = db.Column(db.VARCHAR(5), nullable=False, default='M')
    stock = db.Column(db.Integer, nullable=False, default=0)
