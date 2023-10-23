from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize SQLAlchemy database
db = SQLAlchemy()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DB_NAME = os.getenv("DB_NAME")
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.root_path, DB_NAME)}'

    # Initialize the database within the app
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .vending_Machine import vending_machine
    
    # Register blueprints with distinct URL prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(vending_machine, url_prefix='/')

    from .models import User, Note, VendingMachine

    # Create the database if it doesn't exist
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Define the create_database function to create the database
def create_database(app):
    with app.app_context():
        db.create_all()
        print("Created database")
