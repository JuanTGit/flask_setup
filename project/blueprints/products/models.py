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
    
    def to_dict(self):
        return {
            'id': self.id,
            'prod_name': self.name,
            'price': self.price,
            'image': self.image_url,
            'date_created': self.date_created,
            'category_id': self.category_id
        }
    
    def update(self, data):
        for field in data:
            if field not in {'name', 'price', 'image_url', 'category_id'}:
                continue
            setattr(self, field, data[field])
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship("Product", backref="category")

    def __repr__(self):
        return f"<Category|{self.name}>"
    

