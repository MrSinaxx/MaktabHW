import psycopg2
from typing import List, Tuple
import datetime

class WeatherDatabase:
    def __init__(self):
        # Establish a connection to the PostgreSQL database
        self.connection: psycopg2.extensions.connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='weather_db',
            user='postgres',
            password='motherlode'
        )
        # Create the necessary tables if they don't exist
        self.create_tables()

    def create_tables(self) -> None:
        # Create 'requests' table to store request data
        # Create 'responses' table to store response data
        # Create 'request_counts' table to store request count data
        # Note: If the tables already exist, they are dropped and recreated
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

    # Save the request data to the 'requests' table
    def save_request_data(self, city_name: str, request_time: str) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO requests (city_name, request_time) VALUES (%s, %s)",
                    (city_name, request_time)
                )

    # Save the response data to the 'responses' table
    def save_response_data(self, city_name: str, response_data: dict) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO responses (city_name, temperature, feels_like, last_updated) VALUES (%s, %s, %s, %s)",
                    (city_name, response_data['temperature'], response_data['feels_like'], response_data['last_updated'])
                )

    # Update the request count data in the 'request_counts' table
    def update_request_counts(self) -> None:
        total_requests = self.get_request_count()
        successful_requests = self.get_successful_request_count()
        unsuccessful_requests = self.get_unsuccessful_request_count()

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO request_counts (request_count, successful_request_count, unsuccessful_request_count) VALUES (%s, %s, %s)",
                               (total_requests, successful_requests, unsuccessful_requests))

    # Get the total request count from the 'requests' table
    def get_request_count(self) -> int:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM requests")
                return cursor.fetchone()[0]

    # Get the successful request count from the 'responses' table
    def get_successful_request_count(self) -> int:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM responses")
                return cursor.fetchone()[0]

    # Calculate the unsuccessful request count as the difference between total requests and successful requests
    def get_unsuccessful_request_count(self) -> int:
        total_requests: int = self.get_request_count()
        successful_requests: int = self.get_successful_request_count()
        unsuccessful_requests: int = total_requests - successful_requests
        return unsuccessful_requests

    # Get the requests made in the last hour from the 'requests' table
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

    # Get the request count for each city from the 'requests' table
    def get_city_request_count(self) -> List[Tuple[str, int]]:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT city_name, COUNT(*) FROM requests GROUP BY city_name")
                return cursor.fetchall()

    # Get the latest request counts from the 'request_counts' table
    def get_request_counts(self) -> Tuple[int, int, int]:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT request_count, successful_request_count, unsuccessful_request_count FROM request_counts ORDER BY id DESC LIMIT 1")
                return cursor.fetchone() or (0, 0, 0)

    # Save or update the response data in the 'responses' table
    def save_response_data(self, city_name: str, response_data: dict) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM responses WHERE city_name = %s", (city_name,)
                )
                existing_response = cursor.fetchone()

                if existing_response:
                    cursor.execute(
                        "UPDATE responses SET temperature = %s, feels_like = %s, last_updated = %s WHERE id = %s",
                        (response_data['temperature'], response_data['feels_like'], response_data['last_updated'], existing_response[0])
                    )
                else:
                    cursor.execute(
                        "INSERT INTO responses (city_name, temperature, feels_like, last_updated) VALUES (%s, %s, %s, %s)",
                        (city_name, response_data['temperature'], response_data['feels_like'], response_data['last_updated'])
                    )
        
    # Get the response data for a specific city from the 'responses' table
    def get_response_data(self, city_name: str) -> dict:
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT temperature, feels_like, last_updated FROM responses WHERE city_name = %s",
                    (city_name,)
                )
                return cursor.fetchone()

    # Close the database connection
    def close_connection(self) -> None:
        self.connection.close()
