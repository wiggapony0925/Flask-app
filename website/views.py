from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
#ROUTES WITH IN MY APP

from .models import VendingMachine, db
views = Blueprint("views", __name__)

@views.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
        budget = float(request.form.get('budget'))
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
    
    return render_template("/createMachine.html", title="Create a New Machine", form=VendingMachine())


#edit 
@views.route('/edit_vending_machine/<int:vending_machine_id>', methods=['GET', 'POST'])
@login_required
def edit_vending_machine(vending_machine_id):
    vending_machine = VendingMachine.query.get(vending_machine_id)
    
    #makes sure theres a vending machine
    if vending_machine is None or vending_machine.user_id != current_user.id:
        flash('Vending machine not found', 'error')
        return redirect(url_for('views.home'))



