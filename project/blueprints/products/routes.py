from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import ProductUpdate
from flask_login import login_required, current_user
from .models import Product, Category

products = Blueprint('products', __name__)

@products.route('/product')
@login_required
def product():
    return 'Hello!'

@products.route('/product/<prod_id>')
def product_info(prod_id):
    product = Product.query.get_or_404(prod_id)
    return render_template('product.html', product=product)

@products.route('/product/<prod_id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(prod_id):
    form = ProductUpdate()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    product = Product.query.get_or_404(prod_id)
    if form.validate_on_submit():
        if not current_user.is_admin:
            flash("You don't have permissions to do that.", "danger")
            return redirect(url_for('main.index'))
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
        return redirect(url_for('products.product_edit', prod_id=prod_id))

    return render_template('edit_product.html', product=product, form=form)

@products.route('/product/create', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductUpdate()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if not current_user.is_admin:
        flash("You don't have permissions to do that.", "danger")
        return redirect(url_for('main.index'))
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
        return redirect(url_for('products.product_info', prod_id=new_product.id))



    return render_template('new_product.html', form=form)

@products.route('/product/<prod_id>/delete')
@login_required
def delete_product(prod_id):
    if not current_user.is_admin:
        flash("You don't have permissions to do that.", "danger")
        return redirect(url_for('main.index'))
    product = Product.query.get_or_404(prod_id)
    product.delete()
    flash(f'{product.name} has been deleted', 'danger')
    return redirect(url_for('main.index'))
