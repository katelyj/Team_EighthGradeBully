from database import ScheduleDBManager
import datetime


def convert_to_datetime(period_time):
    period_time_in_datetime_format = datetime.datetime.strptime(period_time, '%I:%M %p')
    return datetime.datetime.combine(datetime.datetime.today(), period_time_in_datetime_format.time())

def in_range(time, period_start_time, period_end_time):
    return period_start_time <= time <= period_end_time

class Schedule:

    def __init__(self, schedule_name):
        self.schedule_name = schedule_name
        self.init_schedule()

    def __str__(self):
        string_form = ''
        for period, period_data in self.schedule.items():
            string_form += '{0: <15} {1: >8} - {2: >8}\n'.format(period, *period_data)
        return string_form

    def init_schedule(self):
        '''
        Retrieve the schedule for the particular instance of Schedule
        '''
        schedule_db_manager = ScheduleDBManager.ScheduleDBManager()
        schedule = schedule_db_manager.get_schedule(self.schedule_name)
        self.schedule = schedule

    def get_schedule(self):
        return self.schedule

    def get_current_period(self):
        current_time = datetime.datetime.now()
        for period, period_times in self.schedule.items():
            period_start_time, period_end_time = map(convert_to_datetime, period_times)
            if in_range(current_time, period_start_time, period_end_time):
                return period
        # We have an error...
