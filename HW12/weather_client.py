import urllib.request
import json
from typing import List, Tuple
from database import WeatherDatabase

database = WeatherDatabase()

def start_client() -> None:
    while True:
        print("1. Get weather information")
        print("2. Exit")
        
        choice: str = input("Enter your choice: ")
        
        if choice == '1':
            get_weather_info()
        elif choice == '2':
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
                print("--------------------------")
                print(f"Feels like: {data['feels_like']}°C")
                print("--------------------------")
                print(f"Last updated: {data['last_updated']}\n")
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
                
                
if __name__ == '__main__':
    start_client()