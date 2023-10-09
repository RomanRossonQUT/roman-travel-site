from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a Blueprint named 'auth' for the authentication routes
authbp = Blueprint('auth', __name__)

# Route for user registration
@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    if register.validate_on_submit():
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        user = db.session.scalar(db.select(User).where(User.name == uname))
        if user:
            flash('Username already exists, please try another')
            return redirect(url_for('auth.register'))
        pwd_hash = generate_password_hash(pwd)
        new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('register.html', form=register, heading='Register')

# Route for user login
@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('login.html', form=login_form, heading='Login')

# Route for user logout (requires authentication)
@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
