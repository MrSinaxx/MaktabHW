import datetime
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'weather_db'
DB_USER = 'postgres'
DB_PASSWORD = 'motherlode'
URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "60be8f85c6c83c4402a1439456f9647c"
CACHE_EXPIRATION_TIME = datetime.timedelta(minutes=10)
SERVER_ADDRESS = "localhost"
PORT = 8000
LOG_FILE_NAME ="weather.log"