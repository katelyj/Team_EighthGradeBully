from collections import OrderedDict
from pymongo import MongoClient

class ScheduleDBManager:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['schedule']

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
