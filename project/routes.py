# Imports flask app from our project __init__ module, so we can set our routes
from project import app
# Used for loading in our templates from html files
from flask import render_template, redirect, url_for
# Forms for users to input data
from project.forms import RegisterForm, LoginForm
from project.models import User
from flask_login import login_user, logout_user, login_required

@app.route('/')
def index():
    # function takes in a template as first arg, and **kwargs
    return render_template('index.html')

# Get for user to recieve data from server, and post for user to submit data from server
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if user exists
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        if user_exists:
            return redirect(url_for('register'))

        # Create a new user instance using form data
        User(username=username, email=email, password=password)


        # Add and commit to the database
        # Added to Users class on creation
            # db.session.add(new_user)
            # db.session.commit()

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            print('Username or Password is incorrect.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
        

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))