from flask import Blueprint, render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
#ROUTES WITH IN MY APP

from .models import Transaction, Note, VendingMachine, db

vending_machine_bp = Blueprint('vending_machine_bp', __name__)

@vending_machine_bp.route('/vending_machine_dashboard/<int:machine_id>')
@login_required
def vending_machine_dashboard(vending_machine_id):
    # Your view logic here
    return render_template("vending_machine_dashboard.html", machine_id=vending_machine_id)


@vending_machine_bp.route('/vending_machine/<int:id>/notes', methods=['POST', 'GET'])
@login_required
def create_notes(id):
    if request.method == 'POST':
        note_content = request.form.get('note')
            
        if len(note_content) < 2:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note_content, user_id=current_user.id, machine_id=id) 
            db.session.add(new_note)
            db.session.commit()
            flash("The note has been added sucessfully", category='error')
            return redirect(url_for('vending_machine_bp.create_notes', id=id)) 


    notes = Note.query.filter_by(vending_machine_id=id).all()
    return render_template('das.html', notes=notes)  