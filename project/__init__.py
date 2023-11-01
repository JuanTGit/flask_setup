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

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'primary'

# We import routes here because It has to be deployed after our flask app
from . import routes, models