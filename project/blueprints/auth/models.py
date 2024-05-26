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
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # kwargs['password'] finds the keyword 'password' passed in kwargs and uses the value as it's paramater. example password=pass123, pass123 is passed in
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()
    
    def save(self, new_password):
        self.password = generate_password_hash(new_password)
        db.session.commit()
    
    def __repr__(self):
        return f'User|{self.username}'
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'admin': self.is_admin,
            'date_created': self.date_created
        }