from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, url_for, redirect, request, flash, get_flashed_messages

from lib.Admin import WeeklyScheduleDBManager
from lib.security import AuthManager, security
from lib.Schedule import Schedule

admin_views = Blueprint('admin_views', __name__)

@admin_views.route('/admin/', methods=['GET'])
def admin():
    return render_template('admin.html', is_logged_in=security.is_logged_in, is_admin=security.is_admin)

@admin_views.route('/save/', methods=['POST'])
def save():
    DAYS = ['mon', 'tues', 'wed', 'thurs', 'fri']
    today_date = datetime.today().date()
    date = (today_date - timedelta(days=today_date.weekday()) - timedelta(days=1)).strftime('%m:%d:%y')
    weekly_schedule_data = {}
    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()

    operation = request.form.get('new') or request.form.get('replace')
    if operation == 'replace':
        pass
    elif operation == 'save':
        for day in DAYS:
            print day
            a_b_day = request.form.get('day_{0}'.format(day))
            schedule_type = request.form.get('schedule_{0}'.format(day))
            weekly_schedule_data[day] = [schedule_type, a_b_day]
        weekly_schedule_db_manager.insert_weekly_schedule(date, weekly_schedule_data)
    return redirect(url_for('admin_views.admin'))
