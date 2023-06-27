import psycopg2
from typing import List, Tuple
import datetime

class WeatherDatabase:
    def __init__(self):
        self.connection: psycopg2.extensions.connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='weather_db',
            user='postgres',
            password='motherlode'
        )
        self.create_tables()

    def create_tables(self) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS requests")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS requests (
                        id SERIAL PRIMARY KEY,
                        city_name TEXT,
                        request_time TIMESTAMP
                    )
                """)

                cursor.execute("DROP TABLE IF EXISTS responses")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS responses (
                        id SERIAL PRIMARY KEY,
                        city_name TEXT,
                        temperature REAL,
                        feels_like REAL,
                        last_updated TIMESTAMP
                    )
                """)

                cursor.execute("DROP TABLE IF EXISTS request_counts")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS request_counts (
                        id SERIAL PRIMARY KEY,
                        request_count INTEGER,
                        successful_request_count INTEGER,
                        unsuccessful_request_count INTEGER
                    )
                """)

    def save_request_data(self, city_name: str, request_time: str) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO requests (city_name, request_time) VALUES (%s, %s)",
                    (city_name, request_time)
                )

    def save_response_data(self, city_name: str, response_data: dict) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO responses (city_name, temperature, feels_like, last_updated) VALUES (%s, %s, %s, %s)",
                    (city_name, response_data['temperature'], response_data['feels_like'], response_data['last_updated'])
                )

    def update_request_counts(self) -> None:
        total_requests = self.get_request_count()
        successful_requests = self.get_successful_request_count()
        unsuccessful_requests = self.get_unsuccessful_request_count()

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO request_counts (request_count, successful_request_count, unsuccessful_request_count) VALUES (%s, %s, %s)",
                               (total_requests, successful_requests, unsuccessful_requests))

    def get_request_count(self) -> int:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM requests")
                return cursor.fetchone()[0]

    def get_successful_request_count(self) -> int:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM responses")
                return cursor.fetchone()[0]

    def get_unsuccessful_request_count(self) -> int:
        total_requests: int = self.get_request_count()
        successful_requests: int = self.get_successful_request_count()
        unsuccessful_requests: int = total_requests - successful_requests
        return unsuccessful_requests

    def get_last_hour_requests(self) -> List[Tuple[str, str]]:
        with self.connection:
            with self.connection.cursor() as cursor:
                current_time = datetime.datetime.now()
                last_hour_time = current_time - datetime.timedelta(hours=1)
                cursor.execute(
                    """
                    SELECT city_name, request_time
                    FROM requests
                    WHERE request_time >= %s AND request_time <= %s
                    """,
                    (last_hour_time, current_time)
                )
                rows = cursor.fetchall()
                last_hour_requests = [
                    (city, str(time))  
                    for city, time in rows
                ]
                return last_hour_requests

    def get_city_request_count(self) -> List[Tuple[str, int]]:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT city_name, COUNT(*) FROM requests GROUP BY city_name")
                return cursor.fetchall()

    def get_request_counts(self) -> Tuple[int, int, int]:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT request_count, successful_request_count, unsuccessful_request_count FROM request_counts ORDER BY id DESC LIMIT 1")
                return cursor.fetchone() or (0, 0, 0)

    def close_connection(self) -> None:
        self.connection.close()
