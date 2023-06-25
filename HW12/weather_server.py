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







def start_server() -> None:
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, WeatherRequestHandler)
    print("Weather server is running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    start_server()