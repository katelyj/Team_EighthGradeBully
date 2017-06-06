from collections import OrderedDict
from pymongo import MongoClient
import datetime

class DayDBManager:

    def __init__(self):
        client = MongoClient()
        self.db = client['day']
        
    def add_days(self, weekday, day):
        self.db.days.insert_one({
            'weekday': weekday, #monday = 0, tuesday = 1... sunday = 6
            'day': day #a, b
        })
        return True
    
    def get_day(self, weekday):
        result = self.db.days.find_one({
            'weekday': weekday
        })
        if result:
            return eval(result.get('day'))
        else:
            return False

    def get_current_day(self):
        today = datetime.today()
        current_day = datetime.weekday(today)

        return True, get_day(self, current_day)
