import collections
import csv
import os

SCHEDULE_CSV_EXTACTER_DIR_NAME = os.path.dirname(__file__) or '.'
DATA_FILE_PATH = os.path.join(SCHEDULE_CSV_EXTACTER_DIR_NAME, '../../data/schedules.csv')

class ScheduleCSVExtracter(object):

    def __init__(self):
        self.data_file = open(DATA_FILE_PATH)
        self.reader = csv.reader(self.data_file)

    def retrieve_schedule(self, schedule_name):
        schedule = collections.OrderedDict()
        for row in self.reader:
            if len(schedule) and row[0] == '':
                break
            if row[0] == 'period' and row[1] == schedule_name:
                period, period_start_time, period_end_time = row[2:]
                period_start_time = period_start_time.replace('a', ' AM')
                period_start_time = period_start_time.replace('p', ' PM')
                period_end_time = period_end_time.replace('a', ' AM')
                period_end_time = period_end_time.replace('p', ' PM')
                schedule[period] = [period_start_time, period_end_time]
        return schedule
