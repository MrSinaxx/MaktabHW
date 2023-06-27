import http.server
import json
import urllib.parse
import datetime
import logging
from urllib.request import urlopen, HTTPError
from http import HTTPStatus
from database import WeatherDatabase
from typing import Optional, Dict, Any, List, Tuple, Union
import time


url: str = "https://api.openweathermap.org/data/2.5/weather"
api_key: str = "60be8f85c6c83c4402a1439456f9647c"

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file: str = "weather.log"
file_handler: logging.FileHandler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

database: WeatherDatabase = WeatherDatabase()
CACHE_EXPIRATION_TIME: datetime.timedelta = datetime.timedelta(minutes=10)


def handle_request(request: http.server.BaseHTTPRequestHandler) -> None:
    parsed_url: urllib.parse.ParseResult = urllib.parse.urlparse(request.path)
    query_params: Dict[str, List[str]] = urllib.parse.parse_qs(parsed_url.query)
    city_name: Optional[List[str]] = query_params.get('city')

    if parsed_url.path == '/database':
        response_data: Optional[Dict[str, Any]] = get_database_data()
        if response_data is None:
            request.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, 'Error retrieving database data')
            logger.error('Error retrieving database data')
        else:
            request.send_response(HTTPStatus.OK)
            request.send_header('Content-Type', 'application/json')
            request.send_header('Access-Control-Allow-Origin', '*')
            request.end_headers()
            request.wfile.write(json.dumps(response_data).encode('utf-8'))
            logger.info('Data retrieved from the database data')

    elif city_name is None or len(city_name) == 0:
        request.send_error(HTTPStatus.BAD_REQUEST, 'Missing city parameter')
        logger.error('Missing city parameter')
    else:
        city_name = city_name[0]
        cache_data: Optional[Tuple[float, float, datetime.datetime]] = database.get_response_data(city_name)

        if cache_data is not None and not is_cache_expired(cache_data[2]):
            response_data: Dict[str, Union[bool, float, str]] = {
                'cache': True,
                'temperature': cache_data[0],
                'feels_like': cache_data[1],
                'last_updated': cache_data[2].strftime('%Y-%m-%d %H:%M:%S')
            }

            logger.info("Reading response from cache")
            request.send_response(HTTPStatus.OK)
            request.send_header('Content-Type', 'application/json')
            request.send_header('Access-Control-Allow-Origin', '*')
            request.end_headers()
            request.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            response_data: Optional[Dict[str, Union[float, str]]] = get_city_weather(city_name)

            if response_data is None:
                request.send_error(HTTPStatus.NOT_FOUND, 'City not found')
                logger.error('City not found')
                database.save_request_data("Invalid City", datetime.datetime.now().isoformat())
            else:
                request.send_response(HTTPStatus.OK)
                request.send_header('Content-Type', 'application/json')
                request.send_header('Access-Control-Allow-Origin', '*')
                request.end_headers()
                request.wfile.write(json.dumps(response_data).encode('utf-8'))
                database.save_request_data(city_name, datetime.datetime.now().isoformat())
                database.save_response_data(city_name, response_data)

    database.update_request_counts()


def is_cache_expired(last_updated: datetime.datetime) -> bool:
    current_time: datetime.datetime = datetime.datetime.now()
    last_updated_str: str = last_updated.strftime('%Y-%m-%d %H:%M:%S')
    cache_time: datetime.datetime = datetime.datetime.strptime(last_updated_str, '%Y-%m-%d %H:%M:%S')
    elapsed_time: datetime.timedelta = current_time - cache_time
    return elapsed_time.total_seconds() >= CACHE_EXPIRATION_TIME.total_seconds()


def send_cached_response(request: http.server.BaseHTTPRequestHandler, cache_data: Dict[str, Union[bool, float, str]]) -> None:
    request.send_response(HTTPStatus.OK)
    request.send_header('Content-Type', 'application/json')
    request.send_header('Access-Control-Allow-Origin', '*')
    request.end_headers()
    request.wfile.write(json.dumps(cache_data).encode('utf-8'))


def get_city_weather(city_name: str) -> Optional[Dict[str, Union[float, str]]]:
    try:
        response = urlopen(f"{url}?q={city_name}&appid={api_key}&units=metric")
        data: Dict[str, Any] = json.loads(response.read().decode('utf-8'))

        if 'main' in data and 'weather' in data:
            weather_data: Dict[str, Union[float, str]] = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            return weather_data

    except HTTPError as e:
        error_message: str = e.read().decode('utf-8')
        logger.error(f"Error retrieving weather data: {error_message}")

    return None


def get_database_data() -> Optional[Dict[str, Union[List[Dict[str, str]], int]]]:
    try:
        last_hour_requests: List[Dict[str, str]] = database.get_last_hour_requests()
        city_request_count: List[Dict[str, Union[str, int]]] = database.get_city_request_count()
        request_count: int
        successful_request_count: int
        unsuccessful_request_count: int
        request_count, successful_request_count, unsuccessful_request_count = database.get_request_counts()

        data: Dict[str, Union[List[Dict[str, str]], int]] = {
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


class WeatherRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        handle_request(self)


def start_server() -> None:
    server_address: Tuple[str, int] = ('localhost', 8000)
    httpd: http.server.HTTPServer = http.server.HTTPServer(server_address, WeatherRequestHandler)
    print("Weather server is running on http://localhost:8000")
    logger.info("Weather server is running on http://localhost:8000")
    httpd.serve_forever()


if __name__ == '__main__':
    start_server()
