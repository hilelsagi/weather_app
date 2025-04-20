import unittest
from unittest.mock import patch, MagicMock
import requests
from backend.api_handler import APIHandler

class TestAPIHandler(unittest.TestCase):

    def setUp(self):
        """Set up an instance of APIHandler before each test."""
        self.api_handler = APIHandler()

    @patch("backend.api_handler.requests.get")
    def test_send_city_request_success(self, mock_get):
        """Test successful city API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"name": "Test City", "latitude": 10.0, "longitude": 20.0}]}
        mock_get.return_value = mock_response

        response = self.api_handler.send_city_request("Test City")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"][0]["name"], "Test City")
        mock_get.assert_called_once_with(
            "https://geocoding-api.open-meteo.com/v1/search?name=Test City&count=1&language=en&format=json",
            timeout=5
        )

    @patch("backend.api_handler.requests.get")
    def test_send_city_request_timeout(self, mock_get):
        """Test timeout handling for city API request."""
        mock_get.side_effect = requests.exceptions.Timeout

        with self.assertRaises(ConnectionError) as cm:
            self.api_handler.send_city_request("Test City")
        
        self.assertEqual(str(cm.exception), "City API request timed out. Please try again.")

    @patch("backend.api_handler.requests.get")
    def test_send_city_request_http_error(self, mock_get):
        """Test HTTP error handling for city API request."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(ConnectionError) as cm:
            self.api_handler.send_city_request("Test City")

        self.assertIn("City API request failed:", str(cm.exception))

    @patch("backend.api_handler.requests.get")
    def test_send_weather_request_success(self, mock_get):
        """Test successful weather API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"hourly": {"temperature_2m": [10, 12, 15]}}
        mock_get.return_value = mock_response

        response = self.api_handler.send_weather_request((10.0, 20.0))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["hourly"]["temperature_2m"], [10, 12, 15])
        mock_get.assert_called_once_with(
            "https://api.open-meteo.com/v1/forecast?latitude=10.0&longitude=20.0&hourly=temperature_2m,relative_humidity_2m&forecast_days=7",
            timeout=5
        )

    @patch("backend.api_handler.requests.get")
    def test_send_weather_request_invalid_coords(self, mock_get):
        """Test handling of invalid coordinates for weather API request."""
        with self.assertRaises(ValueError) as cm:
            self.api_handler.send_weather_request((10.0,))  # Invalid tuple

        self.assertEqual(str(cm.exception), "Invalid coordinates provided. Expected (latitude, longitude).")
        mock_get.assert_not_called()

    @patch("backend.api_handler.requests.get")
    def test_send_weather_request_timeout(self, mock_get):
        """Test timeout handling for weather API request."""
        mock_get.side_effect = requests.exceptions.Timeout

        with self.assertRaises(ConnectionError) as cm:
            self.api_handler.send_weather_request((10.0, 20.0))
        
        self.assertEqual(str(cm.exception), "Weather API request timed out. Please try again.")

if __name__ == "__main__":
    unittest.main()

