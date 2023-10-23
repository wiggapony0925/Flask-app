from flask import Blueprint, render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
#ROUTES WITH IN MY APP

from .models import VendingMachine, db
Vending_Machine = Blueprint('vending_machine', __name__)

@Vending_Machine.route('/calculate', methods={"POST"})
@login_required
def main():
    pass