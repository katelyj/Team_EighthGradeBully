import datetime


#returns current time as a string
def get_cur_time():
    current_time = datetime.datetime.now()
    return current_time.strftime('%I:%M:%S %p')


#returns current date as a string
def get_date():
    return str(datetime.date.today())
