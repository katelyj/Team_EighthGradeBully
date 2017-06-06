from collections import OrderedDict
from pymongo import MongoClient

class DayDBManager:

    def __init__(self):
        client = MongoClient()
        self.db = client['day']

    def add_day(self, day_name, data):
        self.db.schedules.insert_one({
            'day': day_name,
            'data': str(data)
        })
        return True

    def get_day(self, day_name):
        result = self.db.schedules.find_one({
            'day_name': day_name
        })
        if result:
            return eval(result.get('data'))
        else:
            return False