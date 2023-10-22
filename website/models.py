from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    personal_budget = db.Column(db.Integer, nullable=False)
   
    vending_machines = db.relationship("VendingMachine", backref='owner', lazy=True)

class VendingMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    machine_name = db.Column(db.String(80), nullable=False)  # Changed to String
    location = db.Column(db.String(100), nullable=True)  # Added location field
    date = db.Column(db.Date, nullable=True)  # Added date field
    budget = db.Column(db.Float, nullable=False)
    total_sales = db.Column(db.Float, default=0.0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    notes = db.relationship('Note', lazy=True)  # Changed 'Notes' to 'Note'
    transactions = db.relationship('Transaction', backref='vending_machine', lazy=True)  # Changed 'transaction' to 'Transaction'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
