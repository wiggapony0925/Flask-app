from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Transaction, Note, VendingMachine, db

vending_machine_bp = Blueprint('vending_machine_bp', __name__)

# Load the HTML under the selected machine
@vending_machine_bp.route('/vending_machine_dashboard/<int:machine_id>', methods=['GET'])
@login_required
def vending_machine_dashboard(machine_id):
    vending_machine = VendingMachine.query.get(machine_id)
    
    if vending_machine is None or vending_machine.user_id != current_user.id:
        flash("Vending Machine Not Found", category='error')
        return redirect(url_for('views.home', user=current_user))
    
    return render_template("vending_machine_dashboard.html", vending_machine=vending_machine, user=current_user)



# Create a note
@vending_machine_bp.route('/vending_machine_dashboard/<int:id>/notes', methods=['POST', 'GET'])
@login_required
def create_notes(id):
    if request.method == 'POST':
        note_content = request.form.get('note')
            
        if len(note_content) < 2:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note_content, user_id=current_user.id, vending_machine_id=id) 
            db.session.add(new_note)
            db.session.commit()
            flash("The note has been added successfully", category='success')
            return redirect(url_for('vending_machine_bp.create_notes', id=id)) 

    notes = Note.query.filter_by(vending_machine_id=id).all()
    return render_template('das.html', notes=notes)  

# Edit the note
@vending_machine_bp.route('/vending_machine/<int:machine_id>/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(machine_id, note_id):
    pass

# Delete the note
@vending_machine_bp.route('/vending_machine/<int:machine_id>/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(machine_id, note_id):
    pass
