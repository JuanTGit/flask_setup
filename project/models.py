# The models in for our back-end database for us to parse.
from project import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User|{self.username}'
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Coulm(db.Numeric(5, 2), nullable=False)
    image_url = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __repr__(self):
        return f"<Product|{self.name}>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    products = db.relationship("Product", backref="category")

    def __repr__(self):
        return f"<Category|{self.name}>"



    
"""
CREATE USER
flask shell
    user1 = User(username='username', email='email@email.com', password='password')
    db.session.add(user)
    db.session.commit()
    ADDS CREATED USER TO DATABASE

QUERY DATA
https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=endswith#sqlalchemy.schema.Column

    User.query.all() 
    User.query.first() <- Outputs first user
    User.query.filter_by(username='user').first()/.all()
                      Class|Column|Filter
    User.query.filter(User.username *expression* (*filter*)).all()
        expressions:
            User.username.contains('an')
            User.id > 3
            User.id.between(1, 3 )
            User.email.endswith('.com')
        How to do an 'and' == ,
            User.username.startswith('b'), User.id >= 2
        How to do an 'order by'
            User.query.order_by(User.email).all()
            User.query.order_by(User.username).all()
            User.query.order_by(User.username).filter(User.username.contains('b')).all()
        How to do an 'or'
            User.query.filter((User.username.contains('b')) | (User.id == 3)).all()
        How to use 'like'
            users_with_gmail = User.query.filter(User.email.like('%@gmail.com%')).all()

            
"""