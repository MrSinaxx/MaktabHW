import sqlite3
from typing import List, Tuple
import datetime




class WeatherDatabase:
    def __init__(self):
        self.connection: sqlite3.Connection = sqlite3.connect('weather.db')
        self.create_tables()

    def create_tables(self) -> None:
        cursor: sqlite3.Cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT,
                request_time TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT,
                temperature REAL,
                feels_like REAL,
                last_updated TEXT
            )
        """)

        self.connection.commit()
        
    def save_request_data(self, city_name: str, request_time: str) -> None:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute("INSERT INTO requests (city_name, request_time) VALUES (?, ?)", (city_name, request_time))
        self.connection.commit()