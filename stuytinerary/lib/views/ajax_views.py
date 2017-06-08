from flask import Blueprint, jsonify, session
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from lib.Schedule import Schedule, UserScheduleDBManager

ajax_views = Blueprint('ajax_views', __name__)

@ajax_views.route('/schedule_jsonify/<schedule_name>')
def schedule_jsonify(schedule_name):
    return jsonify(Schedule.Schedule(schedule_name).get_schedule_jsonify())

@ajax_views.route('/user_schedule/')
def user_schedule_jsonify():
    return jsonify(UserScheduleDBManager.UserScheduleDBManager().retrieve_user_schedule(session.get('username')))
