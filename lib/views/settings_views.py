from flask import Blueprint, render_template, session, url_for, redirect
import os
import sys

sys.path.insert(0, os.path.abspath("../")) 
from lib.security import AuthManager

settings_views = Blueprint('settings_views', __name__)


@settings_views.route('/settings/', methods = ['GET', 'POST'])
def settings():
    if ("username" in session):
        username = session["username"]
        return render_template('settings.html', user=username, login="True")
    else:
        return render_template('settings.html')

@settings_views.route('/changeschedule/', methods = ['GET', 'POST'])
def change_schedule():
	d = request.form()
	with open('changed_schedule.txt', 'a') as file_:
		file_.write(str(d))

    return redirect(url_for('settings_views.settings'))

@settings_views.route('/changepassword/', methods = ['GET', 'POST'])
def change_password():
    d = request.form()
    old_pass = d['old_pass']
    new_pass = d['new_pass']
    user = session.get('username')
    AuthManager.AuthManager().change_pass(user, old_pass, new_pass)
    return redirect(url_for('settings_views.settings'))
