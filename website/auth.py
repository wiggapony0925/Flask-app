from flask import Blueprint, render_template, request

#ROUTES WITH IN MY APP

auth = Blueprint("auth", __name__)

from flask import Blueprint

auth = Blueprint('auth', __name__)


#/login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', text="Testing ", boolean="True")


#logout
@auth.route("/logout")
def logout():
    return "<h1>logout<h/h1>"


#Register route
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')

