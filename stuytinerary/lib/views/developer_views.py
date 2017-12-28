import datetime
import flask
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from lib.Schedule import SchoolScheduleDBManager, WeeklyScheduleDBManager#, UserScheduleDBManager
from lib.security import AuthManager, security
from lib.WeeklyScheduleScraper import WeeklyScheduleScraper

developer_views = flask.Blueprint('developers_views', __name__)

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
    SchoolScheduleDBManager.SchoolScheduleDBManager().drop_schedules()
    return 'Success!'

@developer_views.route('/populate_database/')
@security.login_required(developer_required=True)
def populate_database():
    SchoolScheduleDBManager.SchoolScheduleDBManager().populate_database()
    return 'Success!'

@developer_views.route('/drop_user/<username>')
@security.login_required(developer_required=True)
def drop_user(username):
    AuthManager.AuthManager().drop_user(username, force=True)
    return 'Success!'

@developer_views.route('/make_admin/<username>')
@security.login_required(developer_required=True)
def add_admin(username):
    AuthManager.AuthManager().make_admin(username, force=True)
    return 'Success!'

@developer_views.route('/del_cookie_attribute/<attribute>')
@security.login_required(developer_required=True)
def del_cookie_attribute(attribute):
    del flask.session[attribute]
    return 'Success!'

@developer_views.route('/show_weekly_schedule_dump/')
@security.login_required(developer_required=True)
def show_weekly_schedule_dump():
    scraper = WeeklyScheduleScraper.WeeklyScheduleScraper('http://stuy.edu')
    info = scraper.get_schedule_info()
    return str(info)
