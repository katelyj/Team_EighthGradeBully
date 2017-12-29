import collections
import datetime
import flask
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from lib.security import AuthManager, security
from lib.Schedule import SchoolScheduleDBManager, WeeklyScheduleDBManager
from lib.utils import admin_utils, utils
from lib.WeeklyScheduleScraper import WeeklyScheduleScraper

admin_views = flask.Blueprint('admin_views', __name__)

@admin_views.route('/admin/', methods=['GET'])
@security.login_required(admin_required=True)
def admin_homepage():
    TODAY_DATE = datetime.datetime.today().date()
    CURRENT_DAY_OF_WEEK = ((TODAY_DATE.weekday() + 1) % 7)
    FIRST_DAY_OF_WEEK = (
        TODAY_DATE - datetime.timedelta(days=CURRENT_DAY_OF_WEEK) - datetime.timedelta(days=0)
    ).strftime('%m/%d/%y')
    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()

    # Test New Feature
    try:
        weekly_schedule_data = admin_utils.get_weekly_schedule()
        admin_utils.insert_into_schedule_database(weekly_schedule_data, True)
    except WeeklyScheduleScraper.WeeklyScheduleScraperException:
        flask.flash('Error: Unable to grab the latest data!')

    weekly_schedule = weekly_schedule_db_manager.get_schedule(FIRST_DAY_OF_WEEK)

    return flask.render_template('admin.html', weekly_schedule=weekly_schedule, is_logged_in=security.logged_in,
                                 is_admin=security.is_admin)

@admin_views.route('/save/', methods=['POST'])
@security.login_required(admin_required=True)
def save_weekly_schedule():
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekly_schedule_data = {'Sunday': ['No School', 'No School'],
                            'Saturday': ['No School', 'No School']}

    for day in WEEKDAYS:
        day_type = flask.request.form.get('{0}_day_type'.format(day))
        schedule_type = flask.request.form.get('{0}_schedule_type'.format(day)) or 'No School'
        weekly_schedule_data[day] = [schedule_type, day_type]

    overwrite = (flask.request.form.get('request_type') == 'Update Weekly Schedule')
    insert_into_schedule_database(weekly_schedule_data, overwrite)
    return flask.redirect(flask.url_for('admin_views.admin_homepage'))

@admin_views.route('/new_or_update_schedule/', methods=['POST'])
@security.login_required(admin_required=True)
def create_new_schedule():
    raw_schedule = json.loads(flask.request.form['new_schedule'])
    new_schedule = collections.OrderedDict()

    new_schedule_name = admin_utils.get_value(raw_schedule[0])
    # Next three after the first field exist for cloning purposes
    for period_data in utils.grouper(raw_schedule[4:], 3):
        period_name, period_start_time, period_end_time = map(admin_utils.get_value, period_data)
        if period_name and period_start_time and period_end_time:
            new_schedule[period_name] = [period_start_time, period_end_time]
        else:
            break

    school_schedule_db_manager = SchoolScheduleDBManager.SchoolScheduleDBManager()
    if school_schedule_db_manager.get_schedule(new_schedule_name):
        school_schedule_db_manager.update_schedule(new_schedule_name, new_schedule)
    else:
        school_schedule_db_manager.add_schedule(new_schedule_name, new_schedule)
    return 'Success!'
