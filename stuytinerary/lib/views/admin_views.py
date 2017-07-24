import datetime
import flask
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from lib.security import AuthManager, security
from lib.Schedule import WeeklyScheduleDBManager

admin_views = flask.Blueprint('admin_views', __name__)

@admin_views.route('/admin/', methods=['GET'])
@security.login_required(admin_required=True)
def admin_homepage():
    TODAY_DATE = datetime.datetime.today().date()
    FIRST_DAY_OF_WEEK = (
        TODAY_DATE - datetime.timedelta(days=TODAY_DATE.weekday()) - datetime.timedelta(days=0)
    ).strftime('%m:%d:%y')
    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()
    weekly_schedule = weekly_schedule_db_manager.get_schedule(FIRST_DAY_OF_WEEK)
    return flask.render_template('admin.html', weekly_schedule=weekly_schedule, is_logged_in=security.logged_in,
                                 is_admin=security.is_admin)

@admin_views.route('/save/', methods=['POST'])
@security.login_required(admin_required=True)
def save_weekly_schedule():
    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    TODAY_DATE = datetime.datetime.today().date()
    FIRST_DAY_OF_WEEK = (
        TODAY_DATE - datetime.timedelta(days=TODAY_DATE.weekday()) - datetime.timedelta(days=0)
    ).strftime('%m:%d:%y')

    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()
    weekly_schedule_data = {'Sunday': ['No School', 'No School'],
                            'Saturday': ['No School', 'No School']}

    for day in DAYS:
        day_type = flask.request.form.get('{0}_day_type'.format(day))
        schedule_type = flask.request.form.get('{0}_schedule_type'.format(day)) or 'No School'
        weekly_schedule_data[day] = [schedule_type, day_type]

    operation = flask.request.form.get('request_type')
    if operation == 'new':
        flask.flash('Schedule Saved!')
        weekly_schedule_db_manager.add_schedule(FIRST_DAY_OF_WEEK, weekly_schedule_data)
    elif operation == 'update':
        flask.flash('Schedule Updated!')
        weekly_schedule_db_manager.update_schedule(FIRST_DAY_OF_WEEK, weekly_schedule_data)
    return flask.redirect(flask.url_for('admin_views.admin_homepage'))
