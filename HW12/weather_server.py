import http.server
import json
import urllib.parse
import datetime
import logging
from urllib.request import urlopen, HTTPError
from http import HTTPStatus
from database import WeatherDatabase
from typing import Optional, Dict, Any, List, Tuple, Union
from config import URL, API_KEY, CACHE_EXPIRATION_TIME, SERVER_ADDRESS, PORT, LOG_FILE_NAME

# Logger class for the weather server
class WeatherServerLogger:
    def __init__(self, name, log_file):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)


# Initialize the logger
logger = WeatherServerLogger(__name__, LOG_FILE_NAME)

# Initialize the weather database
database = WeatherDatabase()


class WeatherRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        city_name = query_params.get('city')

        if parsed_url.path == '/database':
            response_data = self.get_database_data()
        elif city_name is None or len(city_name) == 0:
            self.send_error(HTTPStatus.BAD_REQUEST, 'Missing city parameter')
            logger.error('Missing city parameter')
            return
        else:
            city_name = city_name[0]
            cache_data = database.get_response_data(city_name)

            if cache_data is not None and not self.is_cache_expired(cache_data[2]):
                response_data = {
                    'cache': True,
                    'temperature': cache_data[0],
                    'feels_like': cache_data[1],
                    'last_updated': cache_data[2].strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                response_data = self.get_city_weather(city_name)

                if response_data is None:
                    self.send_error(HTTPStatus.NOT_FOUND, 'City not found')
                    logger.error('City not found')
                    database.save_request_data("Invalid City", datetime.datetime.now().isoformat())
                    return
                else:
                    database.save_request_data(city_name, datetime.datetime.now().isoformat())
                    database.save_response_data(city_name, response_data)

        self.send_json_response(response_data)
        logger.info("Response sent")

        database.update_request_counts()

    def send_json_response(self, data: Optional[Dict[str, Any]]) -> None:
        if data is not None:
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))

    def is_cache_expired(self, last_updated: datetime.datetime) -> bool:
        current_time = datetime.datetime.now()
        elapsed_time = current_time - last_updated
        return elapsed_time.total_seconds() >= CACHE_EXPIRATION_TIME.total_seconds()

    def get_city_weather(self, city_name: str) -> Optional[Dict[str, Union[float, str]]]:
        try:
            response = urlopen(f"{URL}?q={city_name}&appid={API_KEY}&units=metric")
            data = json.loads(response.read().decode('utf-8'))

            if 'main' in data and 'weather' in data:
                weather_data = {
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                return weather_data

        except HTTPError as e:
            error_message = e.read().decode('utf-8')
            logger.error(f"Error retrieving weather data: {error_message}")

        return None

    def get_database_data(self) -> Optional[Dict[str, Union[List[Dict[str, str]], int]]]:
        try:
            last_hour_requests = database.get_last_hour_requests()
            city_request_count = database.get_city_request_count()
            request_count, successful_request_count, unsuccessful_request_count = database.get_request_counts()

            data = {
                'last_hour_requests': last_hour_requests,
                'city_request_count': city_request_count,
                'request_count': request_count,
                'successful_request_count': successful_request_count,
                'unsuccessful_request_count': unsuccessful_request_count
            }

            return data

        except Exception as e:
            logger.error(f"Error retrieving database data: {str(e)}")

        return None


# Start the weather server
def start_server() -> None:
    server_address: Tuple[str, int] = (SERVER_ADDRESS, PORT)
    httpd: http.server.HTTPServer = http.server.HTTPServer(server_address, WeatherRequestHandler)
    print(f"Weather server is running on http://{SERVER_ADDRESS}:{PORT}")
    logger.info(f"Weather server is running on http://{SERVER_ADDRESS}:{PORT}")
    httpd.serve_forever()


if __name__ == '__main__':
    start_server()
