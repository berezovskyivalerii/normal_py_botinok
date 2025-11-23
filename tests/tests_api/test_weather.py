import pytest
import requests
import weather
from weather import get_weather

def test_real_weather_success():
    city = "London"
    result = get_weather(city)
    assert f"The weather in {city} is" in result
    assert result.endswith("°C")

# def test_real_weather_city_not_found():
#     city = "RANDOMCITY_|____.|.___NAME_TRALALALA"
#     with pytest.raises(requests.RequestException):
#         get_weather(city)

# def test_real_response_structure():
#     result = get_weather("Paris")
#     temp_str = result.split(" is ")[1].replace("°C", "")
#     assert float(temp_str)

# def test_missing_api_key_logic():
#     original_key = weather.API_KEY
#     try:
#         weather.API_KEY = None
#         with pytest.raises(ValueError):
#             get_weather("London")
#     finally:
#         weather.API_KEY = original_key

# def test_missing_base_url_logic():
#     original_url = weather.BASE_URL
#     try:
#         weather.BASE_URL = None
#         with pytest.raises(ValueError):
#             get_weather("London")
#     finally:
#         weather.BASE_URL = original_url