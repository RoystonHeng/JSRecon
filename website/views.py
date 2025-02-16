from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route("/delete-note2", methods=["POST"])
def delete_note2():
    try:
        note_data = json.loads(request.data)
        note_id = note_data.get("noteId")

        # Validate note ID
        if not isinstance(note_id, int):
            return jsonify({"success": False, "message": "Invalid note ID."})

        # Fetch the note from the database
        note = Note.query.get(note_id)

        if note:
            # Validate ownership or admin access
            if note.user_id == current_user.id or current_user.is_admin:
                db.session.delete(note)
                db.session.commit()
                return jsonify({"success": True, "message": "Note deleted successfully."})
            else:
                return jsonify({"success": False, "message": "Unauthorized: You cannot delete this note."})

        return jsonify({"success": False, "message": "Note not found."})

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"})
    

@views.route('/add-product', methods=['POST'])
def add_product():
    data = json.loads(request.data)
    isAdmin = data.get('isAdmin', False)  # Safely get value

    print("Admin Status:", isAdmin)  # Debugging

    if isAdmin:
        return jsonify({"success": True, "message": "Product added successfully."})
    
@views.route('/add-product2', methods=['POST'])
def add_product2():
    data = json.loads(request.data)
    isAdmin = data.get('isAdmin', False)  # Safely get value

    print("Admin Status:", isAdmin)  # Debugging

    if isAdmin:
        return jsonify({"success": True, "message": "Product added successfully."})