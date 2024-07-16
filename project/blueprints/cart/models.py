from project import db, login
from datetime import datetime

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)

    def __repr__(self):
        return f"<Cart|ID: {self.id}, User: {self.user_id}>"
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_item(self, product_id, quantity=1):
        existing_item = CartItem.query.filter_by(cart_id=self.id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(cart_id=self.id, product_id=product_id, quantity=quantity)
            db.session.add(new_item)
        db.session.commit()

    def remove_item(self, product_id, quantity=1):
        existing_item = CartItem.query.filter_by(cart_id=self.id, product_id=product_id).first()
        if existing_item:
            if existing_item.quantity > quantity:
                existing_item.quantity -= quantity
            else:
                db.session.delete(existing_item)
            db.session.commit()

    def clear_cart(self):
        for item in self.cart_items:
            db.session.delete(item)
        db.session.commit()

    def update_total(self):
        self.total = sum(item.product.price * item.quantity for item in self.cart_items)
        db.session.commit()

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product = db.relationship('Product', backref='cartitem', lazy=True)

    def __repr__(self):
        return f"<CartItem|ID: {self.id}, Cart: {self.cart_id}, Product: {self.product_id}, Quantity: {self.quantity}>"
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()