from flask import Blueprint, render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
#ROUTES WITH IN MY APP

from .models import VendingMachine, db
views = Blueprint("views", __name__)


#display the current users vending machines
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_vending_machine = VendingMachine.query.filter_by(user_id=current_user.id).all()
    
    return render_template("home.html", user=current_user, vending_machines=user_vending_machine)

@views.route('/create_vending_machine', methods=['POST', 'GET'])
@login_required
def create_vending_machine():
    if request.method == "POST":
        machine_name = request.form.get("machine_name")
        location = request.form.get("location")
        date = request.form.get('date')
        budget = float(request.form.get('location'))
        total_sales = 0 #default sales would start at 0
        
        
    if not machine_name or not budget:
        flash("please fill in all fields", category='error')
    else: 
        new_vending_machine = VendingMachine(
            machine_name=machine_name,
            location=location,
            date =date,
            budget=budget,
            total_sales=total_sales,
            user_id=current_user.id  # Associate with the currently logged-in user
        )
        
        db.session.add(new_vending_machine)
        db.commit()
        
        flash(f"sucessfully added {machine_name} to your portfolio !", category='success')
        return redirect(url_for('views.home'))
