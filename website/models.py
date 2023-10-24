from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

    vending_machines = db.relationship("VendingMachine", backref='owner', lazy=True)

    def calculate_total_budget(self):
        return sum(vm.budget for vm in self.vending_machines)


class VendingMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Float, nullable=False)
    total_sales = db.Column(db.Float, default=0.0, nullable=False)
    description = db.Column(db.Text, default='please add a description', nullable=True)  # Description field added

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    notes = db.relationship('Note', backref='vending_machine', lazy=True)
    transactions = db.relationship('Transaction', backref='vending_machine', lazy=True)

    inventory_items = db.relationship('Inventory', backref='vending_machine', lazy=True)
    expenses = db.relationship('Expense', backref='vending_machine', lazy=True)
    products = db.relationship('Product', backref='vending_machine', lazy=True)
    maintenance_logs = db.relationship('MaintenanceLog', backref='vending_machine', lazy=True)


    def calculate_total_sales(self):
        return sum(tr.amount for tr in self.transactions)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)

# to show month day, time formatted_date_time = created_at.strftime("%B %d, %I:%M %p")

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    amount = db.Column(db.Float, nullable=False)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(1000), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)


class MaintenanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(1000), nullable=False)
    cost = db.Column(db.Float, nullable=True)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.String(500), nullable=False)
