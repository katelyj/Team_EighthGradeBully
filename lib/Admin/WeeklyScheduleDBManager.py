from pymongo import MongoClient

class WeeklyScheduleDBManager(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['weekly_schedule']

    def insert_weekly_schedule(self, date, weekly_schedule_data):
        self.db.weekly_schedules.insert_one({
            'date': date,
            'weekly_schedule_data': str(weekly_schedule_data)
        })
        return True

    def modify_weekly_schedule(self, date, weekly_schedule_data):
        self.db.weekly_schedules.update_one({'date': date}, {'$set': {
            'date': date,
            'weekly_schedule_data': str(weekly_schedule_data)
        }})
        return True

    def retrieve_weekly_schedule(self, date):
        result = self.db.weekly_schedules.find_one({
            'date': date
        })
        if result:
            return eval(result.get('weekly_schedule_data'))
        return None
