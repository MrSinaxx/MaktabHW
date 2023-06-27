import urllib.request
import json
import datetime
from typing import List, Tuple
from database import WeatherDatabase

database = WeatherDatabase()

def start_client() -> None:
    while True:
        print("1. Get weather information")
        print("2. View database")
        print("3. Exit")

        choice: str = input("Enter your choice: ")

        if choice == '1':
            get_weather_info()
        elif choice == '2':
            view_database()
        elif choice == '3':
            break
        else:
            print("Invalid choice")


def get_weather_info() -> None:
    city_name: str = input("Enter a city name: ")
    while True:
        try:
            response = urllib.request.urlopen(f"http://localhost:8000/?city={city_name}")
            data = json.loads(response.read().decode('utf-8'))

            if 'temperature' in data and 'feels_like' in data and 'last_updated' in data:
                print("--------------------------")
                print(f"Temperature: {data['temperature']}°C")
                print(f"Feels like: {data['feels_like']}°C")
                print(f"Last updated: {data['last_updated']}")
                print("--------------------------")
                break
            else:
                print("Invalid response data")

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("City not found")
            else:
                print(f"Error retrieving weather data: {e.reason}")
            choice = input("Enter 'r' to retry or 'b' to go back: ")
            if choice.lower() == 'r':
                city_name = input("Enter a city name: ")
            elif choice.lower() == 'b':
                break
            else:
                print("Invalid choice")

        except urllib.error.URLError as e:
            print(f"Error retrieving weather data: {e.reason}")
            choice = input("Enter 'r' to retry or 'b' to go back: ")
            if choice.lower() == 'r':
                city_name = input("Enter a city name: ")
            elif choice.lower() == 'b':
                break
            else:
                print("Invalid choice")


def view_database() -> None:
    try:
        response = urllib.request.urlopen("http://localhost:8000/database")
        data = json.loads(response.read().decode('utf-8'))

        if 'last_hour_requests' in data and 'city_request_count' in data and 'request_count' in data and 'successful_request_count' in data and 'unsuccessful_request_count' in data:
            last_hour_requests = data['last_hour_requests']
            city_request_counts = data['city_request_count']
            request_count = data['request_count']
            successful_request_count = data['successful_request_count']
            unsuccessful_request_count = data['unsuccessful_request_count']

            print("^--------------------------^")
            print("Last hour requests:")
            for city, time in last_hour_requests:
                print(f"- {city}: {time}")
            print("--------------------------")
            print("City request counts:")
            for city, count in city_request_counts:
                print(f"- {city}: {count}")
            print("--------------------------")
            print(f"Total requests: {request_count}")
            print(f"Successful requests: {successful_request_count}")
            print(f"Unsuccessful requests: {unsuccessful_request_count}")
            print("--------------------------")

        else:
            print("Invalid response data")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Database not found")
        else:
            print(f"Error retrieving database data: {e.reason}")

    except urllib.error.URLError as e:
        print(f"Error retrieving database data: {e.reason}")


if __name__ == '__main__':
    start_client()
