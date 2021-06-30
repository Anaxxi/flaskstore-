from app.extensions import db
from datetime import datetime
from enum import Enum

class EStatus(Enum):
    CREATED = "criado"
    EXPIRED = "expirado"
    ANALYSIS = "em análise"
    COMPLETE = "concluído"
    CARHEBACK = "chargeback"
    PAID = "pago"
    REFUNDED = "reembolsado"
    FAILE = "falha no pagamento"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    item = db.relationship("Item", backref="user", uselist=True)
    profile = db.relationship("Profile", backref=db.backref("user, "), uselist=False)


    def __repr__(self):
        return self.email

class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    document = db.Column(db.String(20), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(20), nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return self.first_name + self.last_name

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(130), nullable=False, unique=True, index=True)
    price = db.Column(db.Float, nullable=False)
    #image = db.Column(db.LargeBinary, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)
    item = db.relationship("Item", backref="product", uselist=True)

    def __repr__(self):
        return self.name


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(35), nullable=False, unique=True, index=True)
    products = db.relationship("Product", backref="categories", uselist=True)

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), default=EStatus.CREATED.value, nullable=False)
    item = db.relationship("Item", backref="order", uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"order number: {self.reference_id}"


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    #def __repr__(self):
    #    return (f"order number: ${self.order.reference_id} quantity: {self.quantity} user: {self.user.profile.first_name} {self.user.profile.last_name} price: {self.price}")
