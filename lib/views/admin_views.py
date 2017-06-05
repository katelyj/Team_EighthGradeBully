from flask import Blueprint, render_template, session, url_for, redirect, request, flash, get_flashed_messages

from lib.security import AuthManager, security
from lib.Schedule import Schedule

admin_views = Blueprint('admin_views', __name__)

@admin_views.route('/admin/', methods = ['GET', 'POST'])
def admin():
    return render_template('admin.html', is_logged_in=security.is_logged_in, is_admin=security.is_admin)

@admin_views.route('/save/', methods = ['GET', 'POST'])
def save():
    return redirect(url_for('admin_views.admin'))
