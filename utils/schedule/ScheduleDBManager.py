from collections import OrderedDict
import os
import sys

sys.path.insert(0, os.path.abspath('../database/'))
print sys.path

from Database import client

class ScheduleDBManager:

    def __init__(self):
        self.db = client['schedule']

    def add_schedule(self, schedule_name, data):
        self.db.schedules.insert_one({
            'schedule_name': schedule_name,
            'data': str(data)
        })
        return

    def get_schedule(self, schedule_name):
        result = self.db.schedules.find_one({
            'schedule_name': schedule_name
        })
        if result:
            return eval(result.get('data'))
        else:
            return

db_manager = ScheduleDBManager()
