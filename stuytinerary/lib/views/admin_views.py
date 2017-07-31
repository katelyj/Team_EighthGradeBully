import collections
import datetime
import flask
import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from lib.security import AuthManager, security
from lib.Schedule import SchoolScheduleDBManager, WeeklyScheduleDBManager

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

    all_schedules_names=SchoolScheduleDBManager.SchoolScheduleDBManager().get_all_schedule_names()
    return flask.render_template('admin.html', weekly_schedule=weekly_schedule, is_logged_in=security.logged_in,
                                 is_admin=security.is_admin, all_schedules_names=all_schedules_names)

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
    if operation == 'New Schedule':
        flask.flash('Schedule Saved!')
        weekly_schedule_db_manager.add_schedule(FIRST_DAY_OF_WEEK, weekly_schedule_data)
    elif operation == 'Update Schedule':
        flask.flash('Schedule Updated!')
        weekly_schedule_db_manager.update_schedule(FIRST_DAY_OF_WEEK, weekly_schedule_data)
    return flask.redirect(flask.url_for('admin_views.admin_homepage'))

def grouper(iterable, group_size, fill_value=None):
    args = [iter(iterable)] * group_size
    return itertools.izip_longest(*args, fillvalue=fill_value)

def get_value(query_string):
    name, value = query_string.split('=')
    value = value.replace('%3A', ':')
    value = value.replace('+', ' ')
    return value

@admin_views.route('/new_schedule/', methods=['POST'])
def create_new_schedule():
    raw_schedule = flask.request.form['new_schedule']
    raw_schedule_as_list = raw_schedule.split('&')
    new_schedule = collections.OrderedDict()

    new_schedule_name = get_value(raw_schedule_as_list[0])
    for period_data in grouper(raw_schedule_as_list[1:], 3):
        period_name, period_start_time, period_end_time = map(get_value, period_data)
        if period_name and period_start_time and period_end_time:
            new_schedule[period_name] = [period_start_time, period_end_time]
        else:
            break
    school_schedule_db_manager = SchoolScheduleDBManager.SchoolScheduleDBManager()
    school_schedule_db_manager.add_schedule(new_schedule_name, new_schedule)
    print new_schedule
    return 'Success!'
