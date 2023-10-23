from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
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


#create
@views.route('/create_vending_machine', methods=['POST', 'GET'])
@login_required
def create_vending_machine():
    if request.method == "POST":
        machine_name = request.form.get("machine_name")
        location = request.form.get("location")
        date_str = request.form.get('date') 
        budget = float(request.form.get('budget'))
        total_sales = 0  # Default sales would start at 0

        if not machine_name or not budget:
            flash("Please fill in all fields", category='error')
        else:
            
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            new_vending_machine = VendingMachine(
                machine_name=machine_name,
                location=location,
                date=date,
                budget=budget,
                total_sales=total_sales,
                user_id=current_user.id  # Associate with the currently logged-in user
            )

            db.session.add(new_vending_machine)
            db.session.commit()

            flash(f"Successfully added {machine_name} to your portfolio!", category='success')
            return redirect(url_for('views.home'))

    return render_template("/createMachine.html", title="Create a New Machine", form=VendingMachine())


#edit 
@views.route('/edit_vending_machine/<int:vending_machine_id>', methods=['GET', 'POST'])
@login_required
def edit_vending_machine(vending_machine_id):
    vending_machine = VendingMachine.query.get(vending_machine_id)
    
    # Makes sure there's a vending machine
    if vending_machine is None or vending_machine.user_id != current_user.id:
        flash('Vending machine not found', 'error')
        return redirect(url_for('views.home'))
    
    if request.method == "POST":
        machine_name = request.form.get('machine_name')
        location = request.form.get('location')
        budget = float(request.form.get('budget'))
        date = request.form.get('date')

        # Update the vending machine's attributes
        vending_machine.machine_name = machine_name
        vending_machine.location = location
        vending_machine.budget = budget
        vending_machine.date = date
        
        db.session.commit()  # Use db.session instead of db

        flash('Vending machine settings updated successfully', 'success')
        return redirect(url_for('views.home'))

    return render_template("edit_vending_machine.html", vending_machine=vending_machine)


#delete
@views.route('/delete_vending_machine/<int:vending_machine_id>', methods=['POST'])
@login_required
def delete_vending_machine(vending_machine_id):
    vending_machine = VendingMachine.query.get(vending_machine_id)
    
    if vending_machine is None or vending_machine.user_id != current_user.id:
        flash('Vending machine not found', 'error')
        return redirect(url_for('views.home'))

    # Delete the vending machine
    db.session.delete(vending_machine)
    db.session.commit()

    flash('Vending machine deleted successfully', 'success')
    return redirect(url_for('views.home'))


