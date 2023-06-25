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
        
    def save_response_data(self, city_name: str, response_data: dict) -> None:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute("INSERT INTO responses (city_name, temperature, feels_like, last_updated) VALUES (?, ?, ?, ?)",
                       (city_name, response_data['temperature'], response_data['feels_like'], response_data['last_updated']))
        self.connection.commit()
        
    def get_request_count(self) -> int:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM requests")
        return cursor.fetchone()[0]

    def get_successful_request_count(self) -> int:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM responses")
        return cursor.fetchone()[0]
    
    def get_unsuccessful_request_count(self) -> int:
        total_requests: int = self.get_request_count()
        successful_requests: int = self.get_successful_request_count()
        unsuccessful_requests: int = total_requests - successful_requests
        return unsuccessful_requests

    def get_last_hour_requests(self) -> List[Tuple[str, str]]:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute("SELECT city_name, request_time FROM requests WHERE request_time > datetime('now', '-1 hour')")
        rows: List[Tuple[str, str]] = cursor.fetchall()

        formatted_rows: List[Tuple[str, str]] = []
        for city, time in rows:
            parsed_time: datetime.datetime = datetime.datetime.fromisoformat(time)
            formatted_time: str = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
            formatted_rows.append((city, formatted_time))

        return formatted_rows
    
    def get_city_request_count(self) -> List[Tuple[str, int]]:
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute("SELECT city_name, COUNT(*) FROM requests GROUP BY city_name")
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()