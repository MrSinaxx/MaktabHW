import datetime
from jdatetime import datetime as jdatetime 


def calculate_time_difference(start_datetime, end_datetime):
    time_difference = end_datetime - start_datetime
    return time_difference.total_seconds()
