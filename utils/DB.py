import csv
import urllib
import os.path


data = open("../data/schedules.csv", "r")
reader = csv.reader(data)

regSched = {}
homeroomSched = {}


#construct dictionary of periods and start/end times
def construct_dicts():
    
    for row in reader:
        if row[0] == "period":

            #regular schedule
            if ( row[1] == "fall-14-a" ):
                regSched[row[2]] = [row[3], row[4]]

            #homeroom schedule
            elif ( row[1] == "fall-14-b" ):
                homeroomSched[row[2]] = [row[3], row[4]]


construct_dicts()


#get period you are currently in
def get_period(curTime, schedule):

    period = ""

    #regular schedule
    if ( schedule == "regular" ):
        for p in regSched.keys():
            startTime = p[0]
            endTime = p[1]
            if ( check_time(startTime, curTime, endTime) ):
                period = p
                break

    #regular schedule
    elif ( schedule == "homeroom" ):
        for p in homeroomSched.keys():
            startTime = p[0]
            endTime = p[1]
            if ( check_time(startTime, curTime, endTime) ):
                period = p
                break

    return period


#check if current time is in between the start and end time
def check_time(startTime, curTime, endTime):
    
    return True
