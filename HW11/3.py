import datetime
from jdatetime import datetime as jdatetime
import pytz

def calculate_time_difference(start_datetime, end_datetime):
    time_difference = end_datetime - start_datetime
    return time_difference.total_seconds()

def count_leap_years(start_year, end_year):
    count = 0
    for year in range(start_year, end_year + 1):
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            count += 1
    return count

def count_clock_changes(start_datetime, end_datetime, time_zone):
    tz = pytz.timezone(time_zone)
    current_datetime = start_datetime
    clock_changes = 0

    while current_datetime < end_datetime:
        try:
            current_offset = tz.utcoffset(current_datetime)
            next_datetime = current_datetime + datetime.timedelta(days=1)
            next_offset = tz.utcoffset(next_datetime)

            if current_offset != next_offset:
                clock_changes += 1

            current_datetime = next_datetime
        except pytz.exceptions.NonExistentTimeError:
            current_datetime += datetime.timedelta(hours=1)

    return clock_changes

def convert_to_hijri_date(gregorian_datetime):
    hijri_datetime = jdatetime.fromgregorian(datetime=gregorian_datetime)
    return hijri_datetime.strftime('%Y/%m/%d %H:%M:%S')

def main():
    start_input = input("Enter the start date and time (YYYY-MM-DD HH:MM:SS): ")
    end_input = input("Enter the end date and time (YYYY-MM-DD HH:MM:SS): ")
    time_zone = input("Enter your time zone (e.g., 'America/New_York'): ")

    start_datetime = datetime.datetime.strptime(start_input, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.datetime.strptime(end_input, "%Y-%m-%d %H:%M:%S")

    time_difference = calculate_time_difference(start_datetime, end_datetime)
    print(f"Time difference: {int(time_difference)} seconds")

    start_year = start_datetime.year
    end_year = end_datetime.year
    leap_year_count = count_leap_years(start_year, end_year)
    print(f"Leap years: {leap_year_count}")

    clock_changes = count_clock_changes(start_datetime, end_datetime, time_zone)
    print(f"Number of clock changes in {time_zone} between {start_datetime} and {end_datetime}: {clock_changes}")

    hijri_start_date = convert_to_hijri_date(start_datetime)
    hijri_end_date = convert_to_hijri_date(end_datetime)
    print(f"Hijri start date: {hijri_start_date}")
    print(f"Hijri end date: {hijri_end_date}")

if __name__ == '__main__':
    main()


#Asia/Tokyo
#Asia/Tehran
