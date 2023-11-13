# Imports flask app from our project __init__ module, so we can set our routes
from project import app, db
# Used for loading in our templates from html files
from flask import render_template, redirect, url_for, flash
# Forms for users to input data
from project.forms import RegisterForm, LoginForm, ProductUpdate, UpdateProfile
from project.models import User, Product, Category, Cart, CartItem
from flask_login import login_user, logout_user, login_required, current_user
from markupsafe import escape


@app.route('/')
def start():
    return render_template('start.html')

@app.route('/index')
def index():
    # function takes in a template as first arg, and **kwargs
    products = Product.query.all()
    # Sort our products by id
    sorted_products = sorted(products, key=lambda x: x.id)
    return render_template('index.html', products=sorted_products)


# Get for user to recieve data from server, and post for user to submit data from server
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if password != form.confirm_pass.data:
            flash('Passwords do not match', 'warning')
            return render_template('register.html', form=form)

        # Check if user exists
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        if user_exists:
            flash(f'User with username {username} or email {email} already exists.', 'danger')
            return redirect(url_for('register'))

        # Create a new user instance using form data
        User(username=username, email=email, password=password)


        # Add and commit to the database
        # Added to Users class on creation
            # db.session.add(new_user)
            # db.session.commit()
        flash(f'Thank you for registering {username}', 'primary')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user_profile = User.query.filter_by(username=username).first()
    form = UpdateProfile()
    if form.validate_on_submit():
        current_pass = form.password.data
        new_password = form.new_password.data

        if user_profile.check_password(current_pass) and new_password == form.confirm_pass.data:
            user_profile.save(new_password)
            flash('Password changed successfully', 'success')
            return redirect(url_for('profile', username=username))
        elif new_password != form.confirm_pass.data:
            flash('Passwords do not match.', 'warning')
            return redirect(url_for('profile', username=username))
        else:
            flash('Current password is incorrect.', 'warning')
            return redirect(url_for('profile', username=username))
        
    return render_template('profile.html', user_profile=user_profile, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Username or Password is incorrect.', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        flash('You have succesfully logged in!', 'success')
        return redirect(url_for('index'))
        

    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have succesfully logged out.', 'dark')
    return redirect(url_for('index'))

@app.route('/product')
@login_required
def product():
    return 'Hello!'

@app.route('/product/<prod_id>')
def product_info(prod_id):
    product = Product.query.get_or_404(prod_id)
    return render_template('product.html', product=product)

@app.route('/product/<prod_id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(prod_id):
    form = ProductUpdate()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    product = Product.query.get_or_404(prod_id)
    if form.validate_on_submit():
        if not current_user.is_admin:
            flash("You don't have permissions to do that.", "danger")
            return redirect(url_for('index'))
        name = form.name.data
        image_url = form.image_url.data
        price = form.price.data
        category = form.category.data

        product.name = name
        product.image_url = image_url
        product.price = price
        product.category_id = category

        product.save()
        flash(f'Successfully Updated { product.name }!', 'success')
        return redirect(url_for('product_edit', prod_id=prod_id))

    return render_template('edit_product.html', product=product, form=form)

@app.route('/product/create', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductUpdate()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if not current_user.is_admin:
        flash("You don't have permissions to do that.", "danger")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        image_url = form.image_url.data
        category = form.category.data

        new_product = Product()
        new_product.name = name
        new_product.price = price
        new_product.image_url = image_url
        new_product.category_id = category

        new_product.create()

        flash(f'{new_product.name} has been created successfully!', 'success')
        return redirect(url_for('product_info', prod_id=new_product.id))



    return render_template('new_product.html', form=form)

@app.route('/product/<prod_id>/delete')
@login_required
def delete_product(prod_id):
    if not current_user.is_admin:
        flash("You don't have permissions to do that.", "danger")
        return redirect(url_for('index'))
    product = Product.query.get_or_404(prod_id)
    product.delete()
    flash(f'{product.name} has been deleted', 'danger')
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:prod_id>')
@login_required
def add_to_cart(prod_id):
    product = Product.query.get(prod_id)
    if product:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()

        cart_item = CartItem(cart_id=cart.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        flash('Product added to the cart successfully!', 'success')
    
    else:
        flash('Product not found!', 'danger')

    return redirect(url_for('index'))

@app.route('/view_cart')
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