import pytest
from database import WeatherDatabase
import datetime


@pytest.fixture(scope="module")
def weather_database():
    db = WeatherDatabase()
    yield db
    db.close_connection()


def test_save_request_data(weather_database):
    city_name = "Test City"
    request_time = "2023-06-27 10:00:00"
    weather_database.save_request_data(city_name, request_time)
    assert weather_database.get_request_count() == 1


def test_save_response_data(weather_database):
    city_name = "Test City"
    response_data = {
        'temperature': 25.5,
        'feels_like': 28.2,
        'last_updated': "2023-06-27 10:05:00"
    }
    weather_database.save_response_data(city_name, response_data)
    assert weather_database.get_successful_request_count() == 1


def test_get_unsuccessful_request_count(weather_database):
    weather_database.save_request_data("Test City", "2023-06-27 09:00:00")
    assert weather_database.get_unsuccessful_request_count() == 1


def test_get_last_hour_requests(weather_database):
    current_time = datetime.datetime.now()
    last_hour_time = current_time - datetime.timedelta(hours=1)
    
    weather_database.save_request_data("City 1", last_hour_time + datetime.timedelta(minutes=15))
    weather_database.save_request_data("City 2", last_hour_time + datetime.timedelta(minutes=30))
    
    weather_database.save_request_data("City 3", last_hour_time - datetime.timedelta(minutes=30))
    
    last_hour_requests = weather_database.get_last_hour_requests()
    assert len(last_hour_requests) == 2


def test_get_city_request_count(weather_database):
    weather_database.save_request_data("City 1", "2023-06-27 11:00:00")
    weather_database.save_request_data("City 2", "2023-06-27 11:30:00")
    weather_database.save_request_data("City 3", "2023-06-27 11:45:00") 
    city_request_count = weather_database.get_city_request_count()
    assert len(city_request_count) == 4

