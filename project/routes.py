from project import app
from flask import render_template, redirect, url_for
from project.forms import RegisterForm

@app.route('/')
def index():
    my_name='Juan'
    count=[1, 2, 3, 4, 5, 6]
    return render_template('index.html', name=my_name, count=count)

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
