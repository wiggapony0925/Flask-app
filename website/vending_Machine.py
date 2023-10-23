from flask import Blueprint, render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
#ROUTES WITH IN MY APP

from .models import VendingMachine, db

vending_machine = Blueprint('vending_machine', __name__)

@vending_machine.route('/vending_machine_dashboard/<int:machine_id>')
@login_required
def vending_machine_dashboard(machine_id):
    # Your view logic here
    return render_template("vending_machine_dashboard.html", machine_id=machine_id)
