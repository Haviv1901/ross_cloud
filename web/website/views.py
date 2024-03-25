from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from flask import redirect
import os
from . import db
from .models import File, User
from flask import current_app as app
from werkzeug.utils import secure_filename
from utilities import *
views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser may submit an empty file without a filename
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)


        # Secure filename and save it to a directory
        filename = secure_filename(file.filename)
        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id) + current_user.username) # dir name: /Storage/[user_id][username]
        os.makedirs(user_dir, exist_ok=True)
        file.save(os.path.join(user_dir, filename))
        
        # Save file to database
        file_path = user_dir + '/' + filename
        new_file = File(file_name = filename, path=file_path, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()

        flash('File uploaded successfully', category='success')
    return render_template("home.html", user=current_user)


@views.route('/files', methods=['GET', 'POST'])
@login_required
def files_page():
    if(request.method == 'POST'):
        user_id = request.form['user_id']
        user = User.query.filter_by(id=user_id).first()
        if(user is not None):
            return render_template("files.html", files=db.session.query(File).filter_by(user_id=user_id).all(), user=user)
        else:
            flash('User not found', category='error')
    return render_template("files.html", files=db.session.query(File).filter_by(user_id=current_user.id).all(), user=current_user)


@views.route('/delete_file', methods=['POST'])
@login_required
def remove_file():
    file_id = request.form['file_id']
    file = File.query.filter_by(id=file_id).first()

    if file is not None:
        db.session.delete(file)
        db.session.commit()
        os.remove(file.path)
        flash('File deleted successfully', category='success')
    else:
        flash('File not found', category='error')

    return render_template("files.html", files=db.session.query(File).filter_by(user_id=current_user.id).all(), user=current_user)


@views.route('/admin')
@login_required
@admin_only
def admin_page():
    return render_template("admin.html", users=User.query.all(), files=File.query.all(), user=current_user)



@views.route('/delete_user', methods=['POST'])
@login_required
@admin_only
def remove_user():
    user_id = request.form['user_id']
    
    if is_user_exist(user_id):
        delete_user(user_id)
        flash('User deleted successfully', category='success')
    else:
        flash('User not found', category='error')
    return render_template("admin.html", users=User.query.all(), files=File.query.all(), user=current_user)

    return render_template("admin.html", users=User.query.all(), files=File.query.all(), user=current_user)