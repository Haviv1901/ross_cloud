from flask import flash, render_template
from flask_login import current_user
from .models import User, File
from . import db
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from .models import User, File
from . import db
from functools import wraps

def check_admin(user):
    return user.admin == True

def is_user_exist(user_id):
    return User.query.filter_by(id=user_id).first() is not None

def delete_user(user_id):
    """
    Deletes a user from the database and all associated files
    Function, does not check if user exist.
    """
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        delete_user_files(user_id)

def delete_user_files(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        files = File.query.filter_by(user_id=user_id).all()
        for file in files:
            db.session.delete(file)
        db.session.commit()


def admin_only(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not check_admin(current_user):
            flash('You are not an admin', category='error')
            return redirect(url_for('views.home'))
        return view_func(*args, **kwargs)
    return wrapper