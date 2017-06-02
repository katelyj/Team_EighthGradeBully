from flask import Blueprint, render_template, session, url_for, redirect


settings_views = Blueprint('settings_views', __name__)


@settings_views.route('/settings', methods = ['GET', 'POST'])
def settings():
    if ("username" in session):
        username = session["username"]
        return render_template('settings.html', user=username, login="True")
    else:
        return render_template('settings.html')

@settings_views.route('/changeschedule/', methods = ['GET', 'POST'])
def change_schedule():
    return redirect(url_for('settings_views.settings'))

@settings_views.route('/changepassword/', methods = ['GET', 'POST'])
def change_password():
    old_pass = session.get('old_pass')
    new_pass = session.get('new_pass')
    return redirect(url_for('settings_views.settings'))
