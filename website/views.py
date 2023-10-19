from flask import Blueprint

#ROUTES WITH IN MY APP

views = Blueprint("views", __name__)


@views.route('/')
def home():
    return "<h1>TEST</h1>"