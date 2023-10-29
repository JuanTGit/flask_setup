# Imports flask app from our project __init__ module, so we can set our routes
from project import app
# Used for loading in our templates from html files
from flask import render_template, redirect, url_for
# Forms for users to input data
from project.forms import RegisterForm

@app.route('/')
def index():
    my_name='Juan'
    count=[1, 2, 3, 4, 5, 6]
    # function takes in a template as first arg, and **kwargs
    return render_template('index.html', name=my_name, count=count)

# Get for user to recieve data from server, and post for user to submit data from server
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')
