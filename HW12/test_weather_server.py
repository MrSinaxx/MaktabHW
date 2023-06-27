import pytest
from unittest.mock import patch, MagicMock
from weather_server import get_city_weather

@patch('weather_server.urlopen')
def test_get_city_weather_valid_city(mock_urlopen):
    city_name = "kish"
    response_data = {
        'main': {'temp': 20.5, 'feels_like': 19.2},
        'weather': [{'description': 'Cloudy'}]
    }
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = '{"main": {"temp": 20.5, "feels_like": 19.2}, "weather": [{"description": "Cloudy"}]}'
    mock_urlopen.return_value = mock_response

    weather_data = get_city_weather(city_name)

    assert weather_data is not None
    assert 'temperature' in weather_data
    assert 'feels_like' in weather_data
    assert 'last_updated' in weather_data

@patch('weather_server.urlopen')
def test_get_city_weather_invalid_city(mock_urlopen):
    city_name = "InvalidCity"
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = '{"cod": "404", "message": "City not found"}'
    mock_urlopen.return_value = mock_response

    weather_data = get_city_weather(city_name)

    assert weather_data is None

@patch('weather_server.urlopen')
def test_get_city_weather_empty_city(mock_urlopen):
    city_name = ""
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = '{"cod": "400", "message": "Missing city parameter"}'
    mock_urlopen.return_value = mock_response

    weather_data = get_city_weather(city_name)

    assert weather_data is None

@patch('weather_server.urlopen')
def test_get_city_weather_no_main_data(mock_urlopen):
    city_name = "tehran"
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = '{"weather": [{"description": "Sunny"}]}'
    mock_urlopen.return_value = mock_response

    weather_data = get_city_weather(city_name)

    assert weather_data is None

@patch('weather_server.urlopen')
def test_get_city_weather_no_weather_data(mock_urlopen):
    city_name = ""
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = '{"main": {"temp": 25.5, "feels_like": 24.2}}'
    mock_urlopen.return_value = mock_response

    weather_data = get_city_weather(city_name)

    assert weather_data is None
