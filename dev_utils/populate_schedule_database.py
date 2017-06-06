import collections
import csv
import sys

sys.path.insert(0, '../')

from lib.Schedule import ScheduleDBManager

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
    list_of_valid_schedules = ['Regular',
                               'Homeroom',]
    schedule_csv_extracter = ScheduleCSVExtracter()
    schedule_db_manager = ScheduleDBManager.ScheduleDBManager()
    schedule_db_manager.drop_schedules()
    for schedule_name in list_of_valid_schedules:
        schedule = schedule_csv_extracter.retrieve_schedule(schedule_name)
        # for period, period_data in schedule.items():
        #     print period, period_data
        schedule_db_manager.add_schedule(schedule_name, schedule)
    return

if __name__ == '__main__':
    main()
