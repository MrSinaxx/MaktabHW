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
            # Send a request to the weather server to get weather information for the specified city
            response = urllib.request.urlopen(f"http://localhost:8000/?city={city_name}")
            data = json.loads(response.read().decode('utf-8'))

            if 'cache' in data and data['cache'] == True:
                print("^--------------------------^")
                print("| Response read from cache |")

            # Check if the response data contains the necessary weather information
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
    while True:
        print("1. View last hour requests")
        print("2. View city request counts")
        print("3. View total request counts")
        print("4. Go back")

        choice: str = input("Enter your choice: ")

        if choice == '1':
            view_last_hour_requests()
        elif choice == '2':
            view_city_request_counts()
        elif choice == '3':
            view_total_request_counts()
        elif choice == '4':
            break
        else:
            print("Invalid choice")


def view_last_hour_requests() -> None:
    try:
        # Send a request to the weather server to get last hour requests information
        response = urllib.request.urlopen("http://localhost:8000/database")
        data = json.loads(response.read().decode('utf-8'))

        if 'last_hour_requests' in data:
            last_hour_requests = data['last_hour_requests']

            print("^--------------------------^")
            print("Last hour requests:")
            for city, time in last_hour_requests:
                print(f"- {city}: {time}")
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


def view_city_request_counts() -> None:
    try:
        # Send a request to the weather server to get city request counts information
        response = urllib.request.urlopen("http://localhost:8000/database")
        data = json.loads(response.read().decode('utf-8'))

        if 'city_request_count' in data:
            city_request_counts = data['city_request_count']

            print("^--------------------------^")
            print("City request counts:")
            for city, count in city_request_counts:
                print(f"- {city}: {count}")
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


def view_total_request_counts() -> None:
    while True:
        print("1. View successful requests")
        print("2. View unsuccessful requests")
        print("3. Go back")

        choice: str = input("Enter your choice: ")

        if choice == '1':
            view_successful_requests()
        elif choice == '2':
            view_unsuccessful_requests()
        elif choice == '3':
            break
        else:
            print("Invalid choice")


def view_successful_requests() -> None:
    try:
        # Send a request to the weather server to get successful requests information
        response = urllib.request.urlopen("http://localhost:8000/database")
        data = json.loads(response.read().decode('utf-8'))

        if 'successful_request_count' in data:
            successful_request_count = data['successful_request_count']

            print("^--------------------------^")
            print("Successful requests:")
            print(f"Count: {successful_request_count}")
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


def view_unsuccessful_requests() -> None:
    try:
        # Send a request to the weather server to get unsuccessful requests information
        response = urllib.request.urlopen("http://localhost:8000/database")
        data = json.loads(response.read().decode('utf-8'))

        if 'unsuccessful_request_count' in data:
            unsuccessful_request_count = data['unsuccessful_request_count']

            print("^--------------------------^")
            print("Unsuccessful requests:")
            print(f"Count: {unsuccessful_request_count}")
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
