from collections import OrderedDict
from pymongo import MongoClient

import os

class ScheduleDBManager:

    DIR_NAME = os.path.dirname(__file__)

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['schedule']
        if not self.db.schedules.count():
            POPULATE_SCHEDULE_DATABASE_PATH = os.path.join(ScheduleDBManager.DIR_NAME, '../../dev_utils/populate_schedule_database.py')
            os.system('python {program_name}'.format(program_name=POPULATE_SCHEDULE_DATABASE_PATH))
            print 'Populated the database'

    def add_schedule(self, schedule_name, data):
        self.db.schedules.insert_one({
            'schedule_name': schedule_name,
            'data': str(data)
        })
        return True

    def get_schedule(self, schedule_name):
        result = self.db.schedules.find_one({
            'schedule_name': schedule_name
        })
        if result:
            return eval(result.get('data'))
        else:
            return False

    def drop_schedules(self):
        self.client.drop_database('schedule')
        self.db = self.client['schedule']
        return True, 'Dropped all schedules!'
