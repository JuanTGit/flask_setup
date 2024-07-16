from flask import Blueprint, jsonify, request
from project import db
from project.blueprints.auth.models import User
from project.blueprints.products.models import Product
from project.blueprints.cart.models import Cart, CartItem
from .auth import basic_auth, token_auth

api = Blueprint('api', __name__, url_prefix='/api')

# Get token
@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token, 'userId': user.id, 'username': user.username, 'is_admin': user.is_admin})

# Get all users
@api.route('/users')
# @token_auth.login_required
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# Get user by id
@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Get all products
@api.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

# Get product by id
@api.route('/products/<id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

# Create, Retreive, Update, Delete

# Create User
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    for field in ["username", "email", "password", "confirm_password"]:
        if field not in data:
            return jsonify({'error': f"You are missing {field} field"}), 400
        if data["password"] != data["confirm_password"]:
            return jsonify({'error': f"Passwords do not match"}), 400
        
    # Grab data from the request body
    username = data["username"]
    email = data["email"]
    password = data["password"]

    user_exists = User.query.filter((User.username==username)|(User.email==email)).all()
    if user_exists:
        return jsonify({'error': f'User with username {username} or email {email} already exists.'}), 400
    
    new_user = User(username=username, email=email, password=password)

    return jsonify(new_user.to_dict())
    


# Update User

@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to update this user'}), 403
    user = User.query.get_or_404(id)
    data = request.json
    if user.check_password(data["currPass"]) == False:
        return jsonify({'error': 'Current Password is incorrect'}), 403
    user.update(data)
    return jsonify({'message': 'Password updated!'}), 200

# Delete User
@api.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id and not current_user.is_admin:
        return jsonify({'error': 'You do not have access to delete this user'}), 403
    user_to_delete = User.query.get_or_404(id)
    user_to_delete.delete()
    return jsonify({'message': 'User deleted successfully'}), 200

# CRUD Products

# Create Product
@api.route('/products', methods=['POST'])
@token_auth.login_required
def create_product():
    user = token_auth.current_user()
    if not user.is_admin:
        return jsonify({'error': 'You do not have access'}), 403
    data = request.json
    
    name = data["name"]
    price = data["price"]
    image = data["image"]
    category_id = data["category_id"]

    new_product = Product(name=name, price=price, image_url=image, category_id=category_id)
    new_product.create()
    return jsonify(new_product.to_dict())
    

# Update Product
@api.route('/products/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_product(id):
    user = token_auth.current_user()
    if not user.is_admin:
        return jsonify({'error': 'You do not have permission to update products'}), 403
    product = Product.query.get_or_404(id)
    data = request.json
    product.update(data)
    return jsonify(product.to_dict())

@api.route('/products/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_product(id):
    user = token_auth.current_user()
    if not user.is_admin:
        return jsonify({'error': 'You do not have permission to delete products'}), 403
    product_to_delete = Product.query.get_or_404(id)
    product_to_delete.delete()
    return jsonify({'message': 'Product deleted successfully'}), 200

# Cart
@api.route('/add-to-cart', methods=['POST'])
@token_auth.login_required
def add_to_cart():
    current_user = token_auth.current_user()
    data = request.json
    product_id = data["product_id"]
    quantity = data.get('quantity', 1)

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    cart.update_total()

    return jsonify({'message': 'Item added to cart', 'total': cart.total})

@api.route('/view-cart', methods=['GET'])
@token_auth.login_required
def view_cart():
    user = token_auth.current_user()

    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        return jsonify({'message': 'Cart not found'})
    
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    items_list = []

    for item in cart_items:
        product = Product.query.get_or_404(item.product_id)
        items_list.append({
            'product_id': item.product_id,
            'product_name': product.name,
            'quantity': item.quantity,
            'price': product.price,
            'total_price': item.quantity * product.price
        })
    
    return jsonify({
        'cart_id': cart.id,
        'user_id': cart.user_id,
        'date_created': cart.datecreated,
        'items': items_list
        })