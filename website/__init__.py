from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os 
from os import path


db = SQLAlchemy()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DB_NAME = os.getenv("DB_NAME")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note, VendingMachine
    
    create_database(app)
    
    return app


def create_database(app):
    if not path("website/" + DB_NAME):
        db.create_all(app=app)
        print("created db")
    
