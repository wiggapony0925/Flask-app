from flask import Blueprint

#ROUTES WITH IN MY APP

auth = Blueprint("auth", __name__)

from flask import Blueprint

auth = Blueprint('auth', __name__)


#/login route
@auth.route('/login')
def login():
    return "<h1>LoginPage</h1>"


#logout
@auth.route("/logout")
def logout():
    return "<h1>Logout</h1>"


#Register route
@auth.route("/sign-up")
def sign_up():
    return "<h1>REGISTER</h1>"