from flask import Blueprint, render_template
from project.blueprints.products.models import Product

main = Blueprint('main', __name__)

@main.route('/')
def start():
    return render_template('start.html')

@main.route('/plans', methods=['GET', 'POST'])
def plans():
    return render_template('plans.html')

@main.route('/index')
def index():
    # function takes in a template as first arg, and **kwargs
    products = Product.query.all()
    # Sort our products by id
    sorted_products = sorted(products, key=lambda x: x.id)
    return render_template('index.html', products=sorted_products)
