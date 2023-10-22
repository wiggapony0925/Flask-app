from flask import Blueprint, render_template, request, flash
import re

auth = Blueprint('auth', __name__)

def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def strong_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
    
    if re.match(pattern, password):
        return True
    else:
        return False

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', text="Testing ", boolean="True")

@auth.route("/logout")
def logout():
    return "<h1>logout<h/h1>"

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        error_messages = []

        if not valid_email(email):
            error_messages.append("Invalid email address")

        if not strong_password(password1) or not strong_password(password2):
            error_messages.append("Password is not strong")

        if len(firstName) < 3:
            error_messages.append("First Name must be at least three characters long")

        if password1 != password2:
            error_messages.append("Both passwords don't match. Please try again")

        if not error_messages:
            # All validation checks passed, proceed to add the user to the database
            # Add your code to add the user to the database here
            # ...

            flash("Registration successful", category='success')
        
        else:
            for message in error_messages:
                flash(message, category='error')

    return render_template('sign_up.html')
