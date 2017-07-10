import datetime

import SchoolScheduleDBManager

def convert_to_datetime(period_time):
    period_time_in_datetime_format = datetime.datetime.strptime(period_time, '%I:%M %p')
    return datetime.datetime.combine(datetime.datetime.today(), period_time_in_datetime_format.time())

def in_range(time, period_start_time, period_end_time):
    return period_start_time <= time <= period_end_time

def seconds_since_midnight(period_time):
    period_time_in_datetime_format = convert_to_datetime(period_time)
    timedelta = datetime.datetime.combine(datetime.datetime.min,
                                          period_time_in_datetime_format.time()) - datetime.datetime.min
    return int(timedelta.total_seconds())

class Schedule:

    def __init__(self, schedule_name):
        self.schedule_name = schedule_name
        self.init_schedule()

    def __str__(self):
        string_form = ''
        for period, period_data in self.schedule.items():
            string_form += '{0: <15} {1: >8} - {2: >8}\n'.format(period, *period_data)
        return string_form

    def __iter__(self):
        self.schedule_periods = self.schedule.keys()
        return self

    def next(self):
        if len(self.schedule_periods):
            period_name = self.schedule_periods.pop(0)
            period_data = self.schedule[period_name]
            return period_name, period_data
        else:
            raise StopIteration

    def init_schedule(self):
        '''
        Retrieve the schedule for the particular instance of Schedule
        '''
        schedule_db_manager = SchoolScheduleDBManager.SchoolScheduleDBManager()
        schedule = schedule_db_manager.get_schedule(self.schedule_name)
        self.schedule = schedule

    def get_current_period(self):
        current_time = datetime.datetime.now()
        for period, period_times in self.schedule.items():
            period_start_time, period_end_time = map(convert_to_datetime, period_time)
            if in_range(current_time, period_start_time, period_end_time):
                return period
        return None

    def get_schedule_jsonify(self):
        json_format = ''
        for period_name, period_times in self.schedule.items():
            period_start_time, period_end_time = map(seconds_since_midnight, period_times)
            json_format += '{0}|{1}|{2}~'.format(period_name, period_start_time, period_end_time)
        return json_format.strip('~')
