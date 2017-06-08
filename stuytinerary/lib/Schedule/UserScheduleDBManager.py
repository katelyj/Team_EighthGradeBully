from pymongo import MongoClient

class UserScheduleDBManager(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['user_schedules']

    def insert_user_schedule(self, username, schedule_data):
        self.db.user_schedule.insert_one({
            'username': username,
            'schedule_data': str(schedule_data)
        })
        return True

    def modify_user_schedule(self):
        self.db.user_schedule.update_one({'username': username}, {'$set': {
            'username': username,
            'schedule_data': str(schedule_data)
        }})
        return True

    def retrieve_user_schedule(self, username):
        result = self.db.user_schedule.find_one({
            'username': username
        })
        if result:
            return result.get('schedule_data')
        return None

    def remove_user_schedule(self, username):
        self.db.user_schedule.delete_one({
            'username': username
        })
        return True
