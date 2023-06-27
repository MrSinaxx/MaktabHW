import http.server
import json
import urllib.parse
import datetime
import logging
from urllib.request import urlopen, HTTPError
from http import HTTPStatus
from database import WeatherDatabase

url = "https://api.openweathermap.org/data/2.5/weather"
api_key = "60be8f85c6c83c4402a1439456f9647c"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file = "weather.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

database = WeatherDatabase()
CACHE_EXPIRATION_TIME = datetime.timedelta(minutes=10)


def handle_request(request):
    parsed_url = urllib.parse.urlparse(request.path)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    city_name = query_params.get('city')

    if parsed_url.path == '/database':
        response_data = get_database_data()
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
        cache_data = database.get_response_data(city_name)

        if cache_data is not None and not is_cache_expired(cache_data[2]):
            response_data = {
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
            response_data = get_city_weather(city_name)

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


def is_cache_expired(last_updated):
    current_time = datetime.datetime.now()
    last_updated_str = last_updated.strftime('%Y-%m-%d %H:%M:%S')
    cache_time = datetime.datetime.strptime(last_updated_str, '%Y-%m-%d %H:%M:%S')
    elapsed_time = current_time - cache_time
    return elapsed_time.total_seconds() >= CACHE_EXPIRATION_TIME.total_seconds()


def send_cached_response(request, cache_data):
    request.send_response(HTTPStatus.OK)
    request.send_header('Content-Type', 'application/json')
    request.send_header('Access-Control-Allow-Origin', '*')
    request.end_headers()
    request.wfile.write(json.dumps(cache_data).encode('utf-8'))


def get_city_weather(city_name):
    try:
        response = urlopen(f"{url}?q={city_name}&appid={api_key}&units=metric")
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


def get_database_data():
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


class WeatherRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)


def start_server():
    server_address = ('localhost', 8000)
    httpd = http.server.HTTPServer(server_address, WeatherRequestHandler)
    print("Weather server is running on http://localhost:8000")
    logger.info("Weather server is running on http://localhost:8000")
    httpd.serve_forever()


if __name__ == '__main__':
    start_server()
