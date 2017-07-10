import datetime

import ScheduleDBManager
import ScheduleCSVExtracter

def convert_to_datetime(period_time):
    period_time_in_datetime_format = datetime.datetime.strptime(period_time, '%I:%M %p')
    return datetime.datetime.combine(datetime.datetime.today(), period_time_in_datetime_format.time())

def seconds_since_midnight(period_time):
    period_time_in_datetime_format = convert_to_datetime(period_time)
    timedelta = datetime.datetime.combine(datetime.datetime.min,
                                          period_time_in_datetime_format.time()) - datetime.datetime.min
    return int(timedelta.total_seconds())

class SchoolScheduleDBManager(ScheduleDBManager.ScheduleDBManager):

    def __init__(self):
        super(SchoolScheduleDBManager, self).__init__('school_schedules')
        if self.get_size() == 0:
            self.populate_database()

    def get_schedule(self, schedule_name, json_format=False):
        schedule = super(SchoolScheduleDBManager, self).get_schedule(schedule_name)
        if not json_format:
            return schedule
        else:
            json_formatted_string = ''
            for period_name, period_times in schedule.items():
                period_start_time, period_end_time = map(seconds_since_midnight, period_times)
                json_formatted_string += '{0}|{1}|{2}~'.format(period_name, period_start_time, period_end_time)
            return json_formatted_string.strip('~')

    def populate_database(self):
        print 'Populating the database...'
        list_of_valid_schedules = ['Regular',
                                   'Homeroom',]
        schedule_csv_extracter = ScheduleCSVExtracter.ScheduleCSVExtracter()
        for schedule_name in list_of_valid_schedules:
            schedule = schedule_csv_extracter.retrieve_schedule(schedule_name)
            self.add_schedule(schedule_name, schedule)
        return
