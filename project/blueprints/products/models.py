from project import db, login
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    image_url = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __repr__(self):
        return f"<Product|{self.name}>"
    
    def save(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship("Product", backref="category")

    def __repr__(self):
        return f"<Category|{self.name}>"