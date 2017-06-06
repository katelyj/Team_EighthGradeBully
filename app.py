from flask import Flask, render_template
import os

from lib.security import security
from lib.Schedule import ScheduleDBManager
from lib.views import ajax_views
from lib.views import public_views
from lib.views import settings_views
from lib.views import admin_views

app = Flask(__name__)
app.secret_key = "patrickchan"
app.register_blueprint(security.security)
app.register_blueprint(ajax_views.ajax_views)
app.register_blueprint(public_views.public_views)
app.register_blueprint(settings_views.settings_views)
app.register_blueprint(admin_views.admin_views)

if __name__ == '__main__':
    os.system('python populate_schedule_database.py')
    print("Schedule Database Reset!\n")
    app.debug = True
    app.run(host='0.0.0.0')
