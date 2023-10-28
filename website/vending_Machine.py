from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Transaction, Note, VendingMachine, db
import json

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


@vending_machine_bp.route('/vending_machine_dashboard/<int:machine_id>/edit_description', methods=['POST', 'GET'])
@login_required
def edit_description(machine_id):
    new_description = request.form.get('description')
    vending_machine = VendingMachine.query.get(machine_id)

    if vending_machine:
        if vending_machine.user_id == current_user.id:
            vending_machine.description = new_description
            db.session.commit()
            flash("Description updated successfully", category='success')
        else:
            flash("You don't have permission to edit this description", category='error')
    else:
        flash("Vending Machine not found", category='error')

    return redirect(url_for('vending_machine_bp.vending_machine_dashboard', machine_id=machine_id))


#add sales
@vending_machine_bp.route('/vending_machine_dashboard/<int:machine_id>/add_sales', methods=['POST'])
@login_required
def add_sales(machine_id):
    if request.method == 'POST':
        sale_amount = float(request.form.get('sale_amount'))
    
        new_sale = Transaction(amount=sale_amount, vending_machine_id=machine_id)
        db.session.add(new_sale)
        db.session.commit()
        
        flash('Sale added successfully', 'success')
        
    return redirect(url_for('vending_machine_bp.vending_machine_dashboard', machine_id=machine_id))

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
   if request.method == 'POST':
       edited_note = request.form.get('edited-note')
       if len(edited_note) < 10:
          flash("this note is still too short", category='error')
          
    
    
    


# Delete the note using json
@vending_machine_bp.route('/vending_machine/<int:machine_id>/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(machine_id, note_id):
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})    