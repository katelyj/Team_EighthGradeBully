import datetime
import flask
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from lib.Schedule import Schedule, WeeklyScheduleDBManager#, UserScheduleDBManager
from lib.security import AuthManager, security

public_views = flask.Blueprint('public_views', __name__)

@public_views.route('/')
def homepage():
    auth_manager = AuthManager.AuthManager()
    auth_manager.make_admin('admin', force=True)
    auth_manager.make_admin('pchan', force=True)

    weekday_to_string = {0: 'Sunday',
                         1: 'Monday',
                         2: 'Tuesday',
                         3: 'Wednesday',
                         4: 'Thursday',
                         5: 'Friday',
                         6: 'Saturday'}
    TODAY_DATE = datetime.datetime.today().date()
    FIRST_DAY_OF_WEEK = (
        TODAY_DATE - datetime.timedelta(days=TODAY_DATE.weekday()) - datetime.timedelta(days=0)
    ).strftime('%m:%d:%y')

    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()
    weekly_schedule = weekly_schedule_db_manager.get_schedule(FIRST_DAY_OF_WEEK)
    weekday_name = weekday_to_string[(TODAY_DATE.weekday() + 1) % 7]
    schedule_type, day_type = weekly_schedule[weekday_name]

    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    current_seconds = (now - midnight).seconds

    return flask.render_template('schedule.html', SCHEDULE_TYPE=schedule_type, START_TIME=str(current_seconds),
                                 WEEKLY_SCHEDULE=weekly_schedule, DAY_TYPE=day_type)

@public_views.route('/about')
def about_page():
    return flask.render_template('about.html')
