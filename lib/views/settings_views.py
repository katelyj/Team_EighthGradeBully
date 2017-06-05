from flask import Blueprint, render_template, session, url_for, redirect, request, flash, get_flashed_messages
import os
import sys

sys.path.insert(0, os.path.abspath("../")) 
from lib.security import AuthManager, security
from lib.Schedule import Schedule

settings_views = Blueprint('settings_views', __name__)


@settings_views.route('/settings/', methods = ['GET', 'POST'])
def settings():
    return render_template('settings.html', is_logged_in=security.is_logged_in, is_admin=security.is_admin)

@settings_views.route('/admin')
def admin():
    return render_template('admin.html', is_logged_in=security.is_logged_in, is_admin=security.is_admin)

@settings_views.route('/changeschedule/', methods = ['GET', 'POST'])
def change_schedule():
    d = request.form()
    with open('changed_schedule.txt', 'a') as file_:
	file_.write(str(d))
    return redirect(url_for('settings_views.settings'))

@settings_views.route('/changepassword/', methods = ['GET', 'POST'])
def change_password():
    old_pass = request.form.get('old_pass')
    new_pass = request.form.get('new_pass')
    conf_new_pass = request.form.get('conf_new_pass')
    user = session.get('username')

    if not new_pass or not old_pass:
        flash('Please fill out all fields!')
        return redirect(url_for('settings_views.settings'))
    else:
        AuthManager.AuthManager().change_pass(user, old_pass, new_pass, conf_new_pass)
        
    return redirect(url_for('settings_views.settings'))
