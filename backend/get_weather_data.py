import json
import requests
from backend.api_handler import APIHandler
from backend.city_parser import CityParser
from backend.weather_parser import WeatherParser
from backend.weekly_weather import WeeklyWeather
def get_weather_data(city):
    """
    Fetches weather data for a given city, processes it, and structures it into weekly forecasts.

    Args:
        city (str): The name of the city for which weather data is requested.

    Returns:
        WeeklyWeather: An object containing the structured weather data.

    Raises:
        ValueError: If the city name is empty or invalid.
        ConnectionError: If there is an issue with API requests (network failure, timeouts).
        json.JSONDecodeError: If an API returns malformed JSON.
    """
    if not city or not isinstance(city, str):
        raise ValueError("City name must be a non-empty string.")

    handler = APIHandler()
    city_parser = CityParser()
    weather_parser = WeatherParser()
    weekly_weather = WeeklyWeather()

    try:
        # Fetch and parse city data
        city_request = handler.send_city_request(city)
        if city_request.status_code != 200:
            raise ConnectionError(f"City API request failed with status {city_request.status_code}")

        city_parser.set_attributes(city_request.content)
        city_coords = city_parser.get_coords()
        if not city_coords:
            raise ValueError("Failed to retrieve coordinates for the city.")

        # Fetch and parse weather data
        weather_request = handler.send_weather_request(city_coords)
        if weather_request.status_code != 200:
            raise ConnectionError(f"Weather API request failed with status {weather_request.status_code}")

        weather_parser.parse_data(weather_request.content)

        # Distribute the data among days
        weekly_times = weather_parser.get_weekly_times()
        weekly_temperatures = weather_parser.get_weekly_temperatures()
        weekly_humidities = weather_parser.get_weekly_humidities()
        city = city_parser.get_city()
        country = city_parser.get_country()

        if not (weekly_times and weekly_temperatures and weekly_humidities and city and country):
            raise ValueError("Incomplete weather data received.")

        weekly_weather.send_data_to_days(weekly_temperatures, weekly_humidities, weekly_times, city, country)
        return weekly_weather

    except requests.exceptions.Timeout:
        raise ConnectionError("The request to the weather API timed out.")
    except requests.exceptions.RequestException as req_err:
        raise ConnectionError(f"Network error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        raise ValueError("Invalid JSON format received from the API.") from json_err  # Preserve JSONDecodeError
    except ValueError:
        raise  # Let ValueError propagate naturally
    except ConnectionError:
        raise  # Let ConnectionError propagate naturally
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")
