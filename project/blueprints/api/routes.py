from flask import Blueprint, jsonify, request
from project.blueprints.auth.models import User
from project.blueprints.products.models import Product
from .auth import basic_auth, token_auth

api = Blueprint('api', __name__, url_prefix='/api')

# Get token
@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token})

# Get all users
@api.route('/users')
# @token_auth.login_required
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# Get user by id
@api.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Get all products
@api.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

# Create, Retreive, Update, Delete

# Create a User
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    # Validate Data
    for field in ["username", "email", "password", "confirm_password"]:
        if field not in data:
            return jsonify({'error': f"You are missing {field} field"}), 400
    if data["password"] != data["confirm_password"]:
        return jsonify({'error': f"Passwords do not match"}), 400
    
    # Grab data from the request body
    username = data["username"]
    email = data["email"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    # Check if username or email already exist in db
    user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
    if user_exists:
        return jsonify({'error': f'User with username {username} or email {email} already exists.'}), 400
    
    # Create new user
    new_user = User(username=username, email=email, password=password)

    return jsonify(new_user.to_dict())

# Update User

@api.route('/users/<id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    pass

# Delete User
@api.route('/users/<id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    pass