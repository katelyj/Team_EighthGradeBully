from flask import Blueprint, jsonify
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
from lib.Schedule import Schedule

ajax_views = Blueprint('ajax_views', __name__)

@ajax_views.route('/schedule_jsonify/<schedule_name>')
def schedule_jsonify(schedule_name):
    return jsonify(Schedule.Schedule(schedule_name).get_schedule_jsonify())
