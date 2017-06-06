import datetime
import DayDBManager

class Day:

    def __init__(self, weekday):
        self.weekday = weekday
        self.init_day()

    def get_current_day(self):
        today = datetime.today()
        current_day = datetime.weekday(today)
        return None
