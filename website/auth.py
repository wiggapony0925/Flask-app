from flask import Blueprint, redirect, render_template, request, flash, url_for
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, db

auth = Blueprint('auth', __name__)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_strong_password(password):
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect email or password', category='error')
    
    return render_template('login.html', user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', category='success')
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already registered', category='error')
        elif not is_valid_email(email):
            flash('Invalid email address', category='error')
        elif not is_strong_password(password1) or not is_strong_password(password2):
            flash('Password is not strong enough', category='error')
        elif len(firstName) < 3:
            flash('First name must be at least three characters long', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='sha256')
            new_user = User(email=email, firstName=firstName, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    
    return render_template('sign_up.html', user=current_user)
