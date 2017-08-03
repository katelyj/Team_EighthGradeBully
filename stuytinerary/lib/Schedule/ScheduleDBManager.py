import os
import pymongo
from collections import OrderedDict


class ScheduleDBManager(object):

    def __init__(self, collection_name):
        self.client = pymongo.MongoClient()

        self.db = self.client['stuytinerary_schedules']
        self.collection_name = collection_name
        self.collection = eval('self.db.{collection_name}'.format(collection_name=collection_name))
        self.db_size = self.collection.count()

    def get_size(self):
        return self.collection.count()

    def add_schedule(self, schedule_name, data):
        self.collection.insert_one({
            'schedule_name': schedule_name,
            'data': str(data)
        })
        return True

    def update_schedule(self, schedule_name, data):
        self.remove_schedule(schedule_name)
        return self.add_schedule(schedule_name, data)

    def remove_schedule(self, schedule_name):
        self.collection.delete_one({
            'schedule_name': schedule_name
        })
        return True

    def get_schedule(self, schedule_name):
        result = self.collection.find_one({
            'schedule_name': schedule_name
        })
        if result:
            return eval(result.get('data'))
        else:
            return False

    def drop_schedules(self):
        self.collection.drop()
        self.collection = eval('self.db.{collection_name}'.format(collection_name=self.collection_name))
        self.db_size = self.collection.count()
        return True, 'Dropped all schedules!'
