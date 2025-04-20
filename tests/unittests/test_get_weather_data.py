import unittest
from unittest.mock import patch, MagicMock
import requests
from backend.get_weather_data import get_weather_data
from backend.weekly_weather import WeeklyWeather

class TestGetWeatherData(unittest.TestCase):

    @patch("backend.get_weather_data.APIHandler")
    @patch("backend.get_weather_data.CityParser")
    @patch("backend.get_weather_data.WeatherParser")
    def test_get_weather_data_success(self, MockWeatherParser, MockCityParser, MockAPIHandler):
        """Test successful retrieval of weather data."""
        
        mock_api_handler = MockAPIHandler.return_value
        mock_city_parser = MockCityParser.return_value
        mock_weather_parser = MockWeatherParser.return_value

        # Mock city API response
        mock_city_api_response = MagicMock()
        mock_city_api_response.status_code = 200
        mock_city_api_response.content = '{"results":[{"name":"Paris","latitude":48.8566,"longitude":2.3522,"country":"France"}]}'
        mock_api_handler.send_city_request.return_value = mock_city_api_response

        # Mock weather API response
        mock_weather_api_response = MagicMock()
        mock_weather_api_response.status_code = 200
        mock_weather_api_response.content = '{"hourly":{"time":["2025-02-08T12:00"] * 168,"temperature_2m":[10.5] * 168,"relative_humidity_2m":[50] * 168}}'
        mock_api_handler.send_weather_request.return_value = mock_weather_api_response

        # Mock city parsing
        mock_city_parser.get_coords.return_value = (48.8566, 2.3522)
        mock_city_parser.get_city.return_value = "Paris"
        mock_city_parser.get_country.return_value = "France"

        # Mock weather parsing
        mock_weather_parser.get_weekly_times.return_value = ["2025-02-08T12:00"] * 168
        mock_weather_parser.get_weekly_temperatures.return_value = [10.5] * 168
        mock_weather_parser.get_weekly_humidities.return_value = [50] * 168

        # Call function
        result = get_weather_data("Paris")

        # Verify result
        self.assertIsInstance(result, WeeklyWeather)  # ✅ FIX: Now `result` is a real `WeeklyWeather` instance

    @patch("backend.get_weather_data.APIHandler")
    def test_get_weather_data_city_api_failure(self, MockAPIHandler):
        """Test failure when city API returns a bad status."""
        
        mock_api_handler = MockAPIHandler.return_value
        mock_city_api_response = MagicMock()
        mock_city_api_response.status_code = 404  # Simulate failure
        mock_api_handler.send_city_request.return_value = mock_city_api_response

        with self.assertRaises(ConnectionError) as cm:
            get_weather_data("Paris")

        self.assertIn("City API request failed with status 404", str(cm.exception))

    @patch("backend.get_weather_data.APIHandler")
    def test_get_weather_data_invalid_json(self, MockAPIHandler):
        """Test handling of invalid JSON response."""

        mock_api_handler = MockAPIHandler.return_value

        # Simulate city API response with invalid JSON
        mock_city_api_response = MagicMock()
        mock_city_api_response.status_code = 200
        mock_city_api_response.content = "INVALID JSON"
        mock_api_handler.send_city_request.return_value = mock_city_api_response

        with self.assertRaises(ValueError) as cm:
            get_weather_data("Paris")

        self.assertIn("Invalid JSON format received in city data.", str(cm.exception))


if __name__ == "__main__":
    unittest.main()

