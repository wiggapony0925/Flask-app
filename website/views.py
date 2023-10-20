from flask import Blueprint, render_template

#ROUTES WITH IN MY APP

views = Blueprint("views", __name__)

@views.route('/')
def home():
    return render_template("home.html")