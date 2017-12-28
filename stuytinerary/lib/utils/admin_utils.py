import datetime
import flask

from lib.Schedule import WeeklyScheduleDBManager
from lib.WeeklyScheduleScraper import WeeklyScheduleScraper

def get_value(dictionary):
    return dictionary.get('value')

def insert_into_schedule_database(weekly_schedule_data, overwrite=False):
    TODAY_DATE = datetime.datetime.today().date()
    CURRENT_DAY_OF_WEEK = ((TODAY_DATE.weekday() + 1) % 7)
    FIRST_DAY_OF_WEEK = (
        TODAY_DATE - datetime.timedelta(days=CURRENT_DAY_OF_WEEK) - datetime.timedelta(days=0)
    ).strftime('%m/%d/%y')

    weekly_schedule_db_manager = WeeklyScheduleDBManager.WeeklyScheduleDBManager()
    if overwrite:
        flask.flash('Schedule Updated!')
        weekly_schedule_db_manager.add_schedule(FIRST_DAY_OF_WEEK, weekly_schedule_data)
    else:
        flask.flash('Schedule Saved!')
        weekly_schedule_db_manager.add_schedule(FIRST_DAY_OF_WEEK, weekly_schedule_data)
    return

def get_weekly_schedule():
    schedule_scraper = WeeklyScheduleScraper.WeeklyScheduleScraper('http://stuy.edu')
    weekly_schedule_data = schedule_scraper.get_schedule_info()
    for day in weekly_schedule_data:
        weekly_schedule_data[day][1] = '{} Day'.format(weekly_schedule_data[day][1].strip('12'))
    weekly_schedule_data['Sunday'] = ['No School', 'No School']
    weekly_schedule_data['Saturday'] = ['No School', 'No School']
    return weekly_schedule_data
