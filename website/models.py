from . import db
from flask_login import UserMixin

class User(db.model, UserMixin):
    pass 


class VendingMachine(db.model):
    pass 