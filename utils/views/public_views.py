import datetime
from flask import Blueprint, render_template, session, url_for

public_views = Blueprint('public_views', __name__)

@public_views.route('/')
def home():
    # schedule = "Regular Schedule"
    # now = datetime.datetime.now()
    # midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # seconds = (now - midnight).seconds
    return render_template('schedule.html')

@public_views.route('/about')
def about():
    if ("username" in session):
        return render_template('about.html', login="True")
    return render_template('about.html')
