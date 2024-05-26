from flask import Blueprint, jsonify
from project.blueprints.auth.models import User
from project.blueprints.products.models import Product

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@api.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@api.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])