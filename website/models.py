from . import db
from flask_login import UserMixin

class User(db.model, UserMixin):
   id = db.Column(db.Integer, primary_key=True, nullable=False)
   email = db.Column(db.String(80), unique=True, nullable=False)
   password = db.Colum(db.String(40), nullable=False)
   budget = db.Colum(db.Integer, nullable=False)
   
   
class VendingMachine(db.model):
    pass 