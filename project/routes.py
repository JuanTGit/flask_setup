from project import app
from flask import render_template

@app.route('/')
def index():
    my_name='Juan'
    count=[1, 2, 3, 4, 5, 6]
    return render_template('index.html', name=my_name, count=count)