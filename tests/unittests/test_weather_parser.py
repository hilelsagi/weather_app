import unittest
import json
from backend.weather_parser import WeatherParser

class TestWeatherParser(unittest.TestCase):

    def setUp(self):
        """Initialize WeatherParser before each test."""
        self.parser = WeatherParser()

    def test_parse_data_valid_json(self):
        """Test parsing valid weather JSON data."""
        json_data = json.dumps({
            "hourly": {
                "time": ["2025-02-08T12:00", "2025-02-09T12:00"],
                "temperature_2m": [10.5, 12.3],
                "relative_humidity_2m": [50, 55]
            }
        })

        self.parser.parse_data(json_data)

        self.assertEqual(self.parser.get_weekly_times(), ["2025-02-08T12:00", "2025-02-09T12:00"])
        self.assertEqual(self.parser.get_weekly_temperatures(), [10.5, 12.3])
        self.assertEqual(self.parser.get_weekly_humidities(), [50, 55])

    def test_parse_data_missing_hourly_key(self):
        """Test handling of missing 'hourly' key in JSON."""
        json_data = json.dumps({
            "wrong_key": {}
        })

        with self.assertRaises(ValueError) as cm:
            self.parser.parse_data(json_data)

        self.assertIn("Missing 'hourly' key in weather data.", str(cm.exception))

    def test_parse_data_incomplete_hourly_data(self):
        """Test handling of missing required keys inside 'hourly'."""
        json_data = json.dumps({
            "hourly": {
                "time": ["2025-02-08T12:00"],
                "temperature_2m": [10.5]  # Missing 'relative_humidity_2m'
            }
        })

        with self.assertRaises(ValueError) as cm:
            self.parser.parse_data(json_data)

        self.assertIn("Incomplete weather data received.", str(cm.exception))

    def test_parse_data_invalid_json_format(self):
        """Test handling of invalid JSON format (raises JSONDecodeError)."""
        invalid_json = "{hourly: {time: [2025-02-08T12:00], temperature_2m: [10.5], relative_humidity_2m: [50]}}"

        with self.assertRaises(ValueError) as cm:
            self.parser.parse_data(invalid_json)

        self.assertIn("Invalid JSON format received in weather data.", str(cm.exception))

    def test_getters_before_parsing(self):
        """Test default values before setting attributes."""
        self.assertEqual(self.parser.get_weekly_times(), [])
        self.assertEqual(self.parser.get_weekly_temperatures(), [])
        self.assertEqual(self.parser.get_weekly_humidities(), [])

if __name__ == "__main__":
    unittest.main()

