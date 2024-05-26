"""
Main file for our flask application
When it comes to configuring and setting up the application we want to
add it to our init file
"""

from flask import Flask
# Config allows for flexibility and security in deployment scenario
from config import Config
# Database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message_category = 'primary'

# app.register_blueprint(auth, url_prefix='/auth')

# We import routes here because It has to be deployed after our flask app
from project.blueprints.auth.routes import auth
from project.blueprints.cart.routes import cart
from project.blueprints.products.routes import products
from project.blueprints.main.routes import main
from project.blueprints.api.routes import api

app.register_blueprint(auth)
app.register_blueprint(cart)
app.register_blueprint(products)
app.register_blueprint(main)
app.register_blueprint(api)