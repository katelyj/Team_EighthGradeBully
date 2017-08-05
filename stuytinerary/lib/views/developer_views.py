from flask import Blueprint, jsonify, session
import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from lib.Schedule import SchoolScheduleDBManager, WeeklyScheduleDBManager#, UserScheduleDBManager
from lib.security import security

developer_views = Blueprint('developers_views', __name__)

@developer_views.route('/remove_schedule/<schedule_name>')
@security.login_required(developer_required=True)
def remove_schedule(schedule_name):
    SchoolScheduleDBManager.SchoolScheduleDBManager().remove_schedule(schedule_name)
    return 'Success!'

@developer_views.route('/list_schedules/')
@security.login_required(developer_required=True)
def list_schedules():
    return str(SchoolScheduleDBManager.SchoolScheduleDBManager().get_all_schedule_names())

@developer_views.route('/drop_schedules/')
@security.login_required(developer_required=True)
def drop_schedules():
    return SchoolScheduleDBManager.SchoolScheduleDBManager().drop_schedules()

@developer_views.route('/populate_database/')
@security.login_required(developer_required=True)
def populate_database():
    return SchoolScheduleDBManager.SchoolScheduleDBManager().populate_database()
