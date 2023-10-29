# Main file for our flask application
from flask import Flask
# Config allows for flexibility and security in deployment scenario
from config import Config
# Database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# We import routes here because It has to be deployed after our flask app
from . import routes, models