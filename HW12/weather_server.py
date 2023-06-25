import http.server
import json
import urllib.parse
import datetime
from urllib.request import urlopen, HTTPError

url: str = "https://api.openweathermap.org/data/2.5/weather"
api_key: str = "60be8f85c6c83c4402a1439456f9647c"


class WeatherRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        city_name = query_params.get('city')
        
        if city_name is None or len(city_name) == 0:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing city parameter')
            return
        

def get_city_weather(self, city_name: str) -> dict:
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








def start_server() -> None:
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, WeatherRequestHandler)
    print("Weather server is running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    start_server()