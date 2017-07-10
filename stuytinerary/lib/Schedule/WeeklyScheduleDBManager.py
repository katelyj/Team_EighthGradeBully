import ScheduleDBManager

class WeeklyScheduleDBManager(ScheduleDBManager.ScheduleDBManager):

    def __init__(self):
        super(WeeklyScheduleDBManager, self).__init__('weekly_schedules')

    def update_schedule(self, date, weekly_schedule_data):
        self.remove_schedule(date)
        return self.add_schedule(date, weekly_schedule_data)
