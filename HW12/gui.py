import urllib.request
import json
import datetime
import tkinter as tk
from typing import List, Tuple
from psycopg2 import connect, sql
from database import WeatherDatabase

database = WeatherDatabase()

def get_weather_info(city_name: str) -> None:
    try:
        response = urllib.request.urlopen(f"http://localhost:8000/?city={city_name}")
        data = json.loads(response.read().decode('utf-8'))

        if 'temperature' in data and 'feels_like' in data and 'last_updated' in data:
            temperature = data['temperature']
            feels_like = data['feels_like']
            last_updated = data['last_updated']

            result_label.configure(text=f"Temperature: {temperature}°C\nFeels like: {feels_like}°C\nLast updated: {last_updated}")
        else:
            result_label.configure(text="Invalid response data")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            result_label.configure(text="City not found")
        else:
            result_label.configure(text=f"Error retrieving weather data: {e.reason}")

    except urllib.error.URLError as e:
        result_label.configure(text=f"Error retrieving weather data: {e.reason}")

def view_database() -> None:
    request_count: int = database.get_request_count()
    successful_request_count: int = database.get_successful_request_count()
    last_hour_requests: List[Tuple[str, str]] = database.get_last_hour_requests()
    city_request_counts: List[Tuple[str, int]] = database.get_city_request_count()

    result_text = f"Request count: {request_count}\n\nSuccessful request count: {successful_request_count}\n\nLast hour requests:\n"
    for city, time in last_hour_requests:
        parsed_time = datetime.datetime.strptime(time.split('.')[0], '%Y-%m-%d %H:%M:%S')
        formatted_time = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
        result_text += f"- {city}: {formatted_time}\n"

    result_text += "\nCity request counts:\n"
    for city, count in city_request_counts:
        result_text += f"- {city}: {count}\n"

    result_label.configure(text=result_text)

def on_submit() -> None:
    city_name = city_entry.get()
    get_weather_info(city_name)

root = tk.Tk()
root.title("Weather Information")

city_label = tk.Label(root, text="Enter a city name:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

submit_button = tk.Button(root, text="Get Weather", command=on_submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

database_button = tk.Button(root, text="View Database", command=view_database)
database_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

root.mainloop()
