from project import db, login
from datetime import datetime

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)

    def __repr__(self):
        return f"<Cart|ID: {self.id}, User: {self.user_id}>"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product = db.relationship('Product', backref='cartitem', lazy=True)

    def __repr__(self):
        return f"<CartItem|ID: {self.id}, Cart: {self.cart_id}, Product: {self.product_id}, Quantity: {self.quantity}>"