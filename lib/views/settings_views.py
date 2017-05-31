from flask import Blueprint, render_template, session, url_for

settings_views = Blueprint('settings_views', __name__)

@settings_views.route('/settings')
def settings():
    if ("username" in session):
        username = session["username"]
        return render_template('settings.html', user=username, login="True")
    else:
        return render_template('settings.html')
