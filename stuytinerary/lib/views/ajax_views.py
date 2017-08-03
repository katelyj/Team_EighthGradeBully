from flask import Blueprint, jsonify, session
import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from lib.Schedule import SchoolScheduleDBManager, WeeklyScheduleDBManager#, UserScheduleDBManager

ajax_views = Blueprint('ajax_views', __name__)

@ajax_views.route('/schedule_jsonify/<schedule_name>')
def schedule_jsonify(schedule_name):
    return jsonify(SchoolScheduleDBManager.SchoolScheduleDBManager().get_schedule(schedule_name, json_format=True))

@ajax_views.route('/user_schedule/')
def user_schedule_jsonify():
    return jsonify(UserScheduleDBManager.UserScheduleDBManager().retrieve_user_schedule(session.get('username')))

@ajax_views.route('/all_schedule_names/')
def all_schedule_names_jsonify():
    return jsonify(SchoolScheduleDBManager.SchoolScheduleDBManager().get_all_schedule_names())

@ajax_views.route('/weekly_schedule/')
def get_weekly_schedule():
    TODAY_DATE = datetime.datetime.today().date()
    FIRST_DAY_OF_WEEK = (
        TODAY_DATE - datetime.timedelta(days=TODAY_DATE.weekday()) - datetime.timedelta(days=0)
    ).strftime('%m:%d:%y')
    weekday_to_string = {0: 'Sunday',
                         1: 'Monday',
                         2: 'Tuesday',
                         3: 'Wednesday',
                         4: 'Thursday',
                         5: 'Friday',
                         6: 'Saturday'}

    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()
    weekly_schedule = weekly_schedule_db_manager.get_schedule(FIRST_DAY_OF_WEEK)
    weekday_name = weekday_to_string[(TODAY_DATE.weekday() + 1) % 7]
    return jsonify(weekly_schedule)
