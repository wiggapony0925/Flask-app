from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.model, UserMixin):
   id = db.Column(db.Integer, primary_key=True, nullable=False)
   email = db.Column(db.String(80), unique=True, nullable=False)
   password = db.Colum(db.String(40), nullable=False)
   personal_budget = db.Colum(db.Integer, nullable=False)
   
   vendind_machines = db.relationship("VendingMachine", backref='owner', lazy=True)
   
class VendingMachine(db.model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    machine_name = db.Column(db.Integer, nullable=False)
    total_sales = db.Column(db.Float, default=0.0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    
    #assosiations
    
class vendingMachine_data(db.model):
    pass

