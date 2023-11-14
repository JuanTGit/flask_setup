from flask import Blueprint, render_template, redirect, url_for, flash
from project import db
from flask_login import login_required, current_user
from .models import Cart, CartItem
from project.blueprints.products.models import Product

cart = Blueprint('cart', __name__)

@cart.route('/add_to_cart/<int:prod_id>')
@login_required
def add_to_cart(prod_id):
    product = Product.query.get(prod_id)
    if product:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        
        # Check if the product is already in the cart
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()

        if cart_item:
            # If the product is already in the cart, update the quantity
            cart_item.quantity += 1
            flash('Quantity updated in the cart successfully!', 'success')
        else:
            # If the product is not in the cart, add a new item
            cart_item = CartItem(cart_id=cart.id, product_id=product.id)
            db.session.add(cart_item)
            flash('Product added to the cart successfully!', 'success')

        db.session.commit()
    else:
        flash('Product not found!', 'danger')

    return redirect(url_for('main.index'))

@cart.route('/view_cart')
@login_required
def view_cart():
    # Implement a route to display the contents of the cart
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        return render_template('cart.html', cart=cart, cart_items=cart_items)
    else:
        flash('Cart is empty!', 'info')
        return render_template('cart.html', cart=None, cart_items=None)