import flask
import functools

import AuthManager
from security_utils import redirect_back

security = flask.Blueprint('security', __name__)
db_manager = AuthManager.AuthManager()

def login_required(admin_required=False, developer_required=False):
    def actual_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            if is_logged_in(admin_required, developer_required):
                return function(*args, **kwargs)
            else:
                flask.session['next'] = flask.request.url
                return flask.redirect(flask.url_for('security.login_form'))
        return wrapper
    return actual_decorator

def is_admin():
    username = flask.session.get('username')

    if not username:
        return False
    elif db_manager.is_registered(username) and db_manager.is_admin(username):
        return True
    else:
        return False

def is_logged_in(admin_required=False, developer_required=False):
    username = flask.session.get('username')

    if not username:
        return False
    elif developer_required and db_manager.is_developer(username):
        return True
    elif admin_required and db_manager.is_admin(username):
        return True
    elif not (admin_required or developer_required) and db_manager.is_registered(username):
        return True
    elif (admin_required and not db_manager.is_admin(username)) or (developer_required and not db_manager.is_developer(username)):
        return False
    else:
        flask.session.pop('username')
        return False

@security.route('/logged_in/')
def logged_in():
    return flask.jsonify(result=True if flask.session.get('username') else False)

@security.route('/register/')
def register_form():
    if is_logged_in():
        return flask.redirect(flask.url_for('public_views.homepage'))
    else:
        return flask.render_template('register.html')

@security.route('/register/', methods = ['POST'])
def register():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    confirm_password = flask.request.form.get('confirm_password')

    if not username or not password or not confirm_password:
        flask.flash('Please fill out all fields!')
        return flask.redirect(flask.url_for('security.register_form'))

    results = db_manager.register(username, password, confirm_password)
    print results
    flask.flash(results[1])

    if results[0]:
        return flask.redirect(flask.url_for('security.login_form'))
    else:
        return flask.redirect(flask.url_for('security.register_form'))

@security.route('/login/')
def login_form():
    if is_logged_in():
        return flask.redirect(flask.url_for('public_views.homepage'))
    else:
        return flask.render_template('login.html')

@security.route('/login/', methods=['POST'])
def login():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    if not username or not password:
        flask.flash('Please fill out all fields!')
        return flask.redirect(flask.url_for('security.login_form'))
    else:
        results = db_manager.login(username, password)

        if results[0]:
            flask.session['username'] = username
            return redirect_back()
        else:
            flask.flash(results[1])
            return flask.redirect(flask.url_for('security.login_form'))

@security.route('/logout/')
def logout():
    if is_logged_in():
        flask.session.pop('username')

        if 'next' in flask.session:
            flask.session.pop('next')

    return flask.redirect(flask.url_for('public_views.homepage'))
