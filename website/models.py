from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Add a foreign key reference to VendingMachine
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)

    # Define a relationship to VendingMachine
    vending_machine = db.relationship('VendingMachine', backref='notes')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    personal_budget = db.Column(db.Integer, nullable=False)

    vending_machines = db.relationship("VendingMachine", backref='owner', lazy=True)


class VendingMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    machine_name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Float, nullable=False)
    total_sales = db.Column(db.Float, default=0.0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    notes = db.relationship('Note', lazy=True)
    transactions = db.relationship('Transaction', backref='vending_machine', lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
