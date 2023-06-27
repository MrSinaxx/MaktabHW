import http.server
import json
import urllib.parse
import datetime
from urllib.request import urlopen, HTTPError
from http import HTTPStatus
from psycopg2 import connect, sql
from database import WeatherDatabase

url = "https://api.openweathermap.org/data/2.5/weather"
api_key = "60be8f85c6c83c4402a1439456f9647c"

database = WeatherDatabase()

def handle_request(request):
    parsed_url = urllib.parse.urlparse(request.path)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    city_name = query_params.get('city')

    if city_name is None or len(city_name) == 0:
        request.send_error(HTTPStatus.BAD_REQUEST, 'Missing city parameter')
        return

    city_name = city_name[0]
    response_data = get_city_weather(city_name)

    if response_data is None:
        request.send_error(HTTPStatus.NOT_FOUND, 'City not found')

        database.save_request_data("Invalid City", datetime.datetime.now().isoformat())
        return

    request.send_response(HTTPStatus.OK)
    request.send_header('Content-Type', 'application/json')
    request.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
    request.end_headers()
    request.wfile.write(json.dumps(response_data).encode('utf-8'))

    database.save_request_data(city_name, datetime.datetime.now().isoformat())
    database.save_response_data(city_name, response_data)

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
        print(f"Error retrieving weather data: {error_message}")

    return None

class WeatherRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)

def start_server():
    server_address = ('localhost', 8000)
    httpd = http.server.HTTPServer(server_address, WeatherRequestHandler)
    print("Weather server is running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    start_server()
