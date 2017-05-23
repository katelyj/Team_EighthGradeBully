import datetime
from flask import Blueprint, render_template

public_views = Blueprint('public_views', __name__)

@public_views.route('/')
def home():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    #seconds = 31490 #second period
    #seconds = 37190 #Passing
    #seconds = 52000 #9th period
    #seconds = 55000 #10th period
    #seconds = 56100 #switching to afterschool
    #seconds = 28800 #beginning of the day
    return render_template('schedule.html', starttime=str(seconds), schedulename='Regular Schedule')

@public_views.route('/about')
def about():
    return render_template('about.html')
