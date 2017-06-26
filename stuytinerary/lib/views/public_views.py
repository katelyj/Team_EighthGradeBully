from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, url_for
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from lib.Admin import WeeklyScheduleDBManager
from lib.Schedule import Schedule, UserScheduleDBManager
from lib.security import AuthManager, security

public_views = Blueprint('public_views', __name__)

@public_views.route('/')
def home():
    auth_manager = AuthManager.AuthManager()
    auth_manager.make_admin('admin', force=True)

    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds

    weekday_to_string = {0: 'sun',
                         1: 'mon',
                         2: 'tues',
                         3: 'wed',
                         4: 'thurs',
                         5: 'fri',
                         6: 'sat'}
    today_date = datetime.today().date()
    date = (today_date - timedelta(days=today_date.weekday()) - timedelta(days=1)).strftime('%m:%d:%y')

    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()
    weekly_schedule = weekly_schedule_db_manager.retrieve_weekly_schedule(date)
    print date
    print weekly_schedule
    weekday_name = weekday_to_string[today_date.weekday() + 1]
    weekday_name = 'mon'
    if weekday_name == 'sat' or weekday_name == 'sun':
        weekly_schedule = None

    raw_user_schedule = UserScheduleDBManager.UserScheduleDBManager().retrieve_user_schedule(session.get('username'))

    if (weekly_schedule == None):
        return render_template('schedule.html', SCHEDULE_NAME=None, starttime=str(seconds), today_data=None, weekly_schedule=None, schedule=None, a_b_day=None, is_logged_in=security.is_logged_in, is_admin=security.is_admin)

    else:
        today_data = weekly_schedule[weekday_name]
        print(weekly_schedule)
        schedule = Schedule.Schedule(today_data[0])
        a_b_day = today_data[1]
        return render_template('schedule.html', SCHEDULE_NAME=today_data[0], starttime=str(seconds), today_data=today_data, weekly_schedule=weekly_schedule, schedule=schedule, a_b_day=a_b_day, is_logged_in=security.is_logged_in, is_admin=security.is_admin)

@public_views.route('/about')
def about():
    return render_template('about.html', is_logged_in=security.is_logged_in, is_admin=security.is_admin)