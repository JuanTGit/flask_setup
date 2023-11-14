from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegisterForm, LoginForm, UpdateProfile
from flask_login import login_user, logout_user, login_required
from .models import User



auth = Blueprint('auth', __name__)

# Get for user to recieve data from server, and post for user to submit data from server
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if password != form.confirm_pass.data:
            flash('Passwords do not match', 'warning')
            return render_template('register.html', form=form)

        # Check if user exists
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        if user_exists:
            flash(f'User with username {username} or email {email} already exists.', 'danger')
            return redirect(url_for('auth.register'))

        # Create a new user instance using form data
        User(username=username, email=email, password=password)


        # Add and commit to the database
        # Added to Users class on creation
            # db.session.add(new_user)
            # db.session.commit()
        flash(f'Thank you for registering {username}', 'primary')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user_profile = User.query.filter_by(username=username).first()
    form = UpdateProfile()
    if form.validate_on_submit():
        current_pass = form.password.data
        new_password = form.new_password.data

        if user_profile.check_password(current_pass) and new_password == form.confirm_pass.data:
            user_profile.save(new_password)
            flash('Password changed successfully', 'success')
            return redirect(url_for('auth.profile', username=username))
        elif new_password != form.confirm_pass.data:
            flash('Passwords do not match.', 'warning')
            return redirect(url_for('auth.profile', username=username))
        else:
            flash('Current password is incorrect.', 'warning')
            return redirect(url_for('auth.profile', username=username))
        
    return render_template('profile.html', user_profile=user_profile, form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Username or Password is incorrect.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('You have succesfully logged in!', 'success')
        return redirect(url_for('main.index'))
        

    return render_template('login.html', form=form)



@auth.route('/logout')
def logout():
    logout_user()
    flash('You have succesfully logged out.', 'dark')
    return redirect(url_for('main.index'))
