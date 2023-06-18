import datetime
from jdatetime import datetime as jdatetime 


def calculate_time_difference(start_datetime, end_datetime):
    time_difference = end_datetime - start_datetime
    return time_difference.total_seconds()

def count_leap_years(start_year, end_year):
    for year in range(start_year, end_year + 1):
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            count += 1
    return count

def change_clock(start_datetime, end_datetime):
    if start_datetime.utcoffset() != end_datetime.utcoffset():
        return "Clock change detected"
    else:
        return "No clock change detected"