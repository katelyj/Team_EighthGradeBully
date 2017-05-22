import collections
import csv
import sys

sys.path.insert(0, '../')

from utils.database import ScheduleDBManager

class ScheduleCSVExtracter:

    def __init__(self):
        self.data_file = open('../data/schedules.csv')
        self.reader = csv.reader(self.data_file)

    def retrieve_schedule(self, schedule_name):
        schedule = collections.OrderedDict()
        for row in self.reader:
            if row[0] == 'period' and row[1] == schedule_name:
                period, period_start_time, period_end_time = row[2:]
                period_start_time = period_start_time.replace('a', ' AM')
                period_start_time = period_start_time.replace('p', ' PM')
                period_end_time = period_end_time.replace('a', ' AM')
                period_end_time = period_end_time.replace('p', ' PM')
                schedule[period] = [period_start_time, period_end_time]
                if 'After school' in schedule:
                    break
        return schedule

def main():
    list_of_valid_schedules = ['fall-14-regular',
                               'fall-14-homeroom',]
    schedule_csv_extracter = ScheduleCSVExtracter()
    for schedule_name in list_of_valid_schedules:
        schedule = schedule_csv_extracter.retrieve_schedule(schedule_name)
        # for period, period_data in schedule.items():
        #     print period, period_data
        ScheduleDBManager.db_manager.add_schedule(schedule_name, schedule)
    return

if __name__ == '__main__':
    main()
