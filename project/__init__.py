from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'You will never guess.'

from . import routes