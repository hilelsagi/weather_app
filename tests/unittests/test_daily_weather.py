import unittest
from datetime import datetime
from backend.daily_weather import DailyWeather  

class TestDailyWeather(unittest.TestCase):

    def setUp(self):
        """Initialize DailyWeather before each test."""
        self.weather = DailyWeather()

    def test_set_attributes_valid_data(self):
        """Test setting attributes with valid data."""
        times = ["2025-02-08T12:00", "2025-02-08T18:00"]
        temperatures = [5.0, 12.0, 10.0, 8.0]
        humidities = [50, 55, 60, 65]

        self.weather.set_attributes(times, temperatures, humidities)

        self.assertEqual(self.weather.get_date(), "08-02-2025")
        self.assertEqual(self.weather.get_name(), "Saturday")
        self.assertEqual(self.weather.get_night(), 5.0)  # Min temp
        self.assertEqual(self.weather.get_day(), 12.0)   # Max temp
        self.assertEqual(self.weather.get_humidity(), 57.5)  # Average humidity

    def test_set_attributes_empty_lists(self):
        """Test handling of empty lists."""
        with self.assertRaises(ValueError) as cm:
            self.weather.set_attributes([], [10.0, 12.0], [50, 55])

        self.assertIn("Invalid or empty 'times' list provided.", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            self.weather.set_attributes(["2025-02-08T12:00"], [], [50, 55])

        self.assertIn("Invalid or empty 'temperatures' list provided.", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            self.weather.set_attributes(["2025-02-08T12:00"], [10.0, 12.0], [])

        self.assertIn("Invalid or empty 'humidities' list provided.", str(cm.exception))

    def test_set_attributes_malformed_date(self):
        """Test handling of malformed date format."""
        malformed_times = ["08-02-2025T12:00"]  # Incorrect format

        with self.assertRaises(ValueError) as cm:
            self.weather.set_attributes(malformed_times, [10.0, 12.0], [50, 55])

        self.assertIn("Error processing weather data", str(cm.exception))

    def test_getters_before_setting(self):
        """Test default values before setting attributes."""
        self.assertEqual(self.weather.get_date(), "")
        self.assertEqual(self.weather.get_name(), "")
        self.assertEqual(self.weather.get_night(), 0.0)
        self.assertEqual(self.weather.get_day(), 0.0)
        self.assertEqual(self.weather.get_humidity(), 0.0)

    def test_str_representation(self):
        """Test string representation of the weather object."""
        times = ["2025-02-08T12:00", "2025-02-08T18:00"]
        temperatures = [5.0, 12.0, 10.0, 8.0]
        humidities = [50, 55, 60, 65]

        self.weather.set_attributes(times, temperatures, humidities)

        expected_str = "Saturday, 08-02-2025: Day: 12.0°C, Night: 5.0°C, Humidity: 57.5%"
        self.assertEqual(str(self.weather), expected_str)

if __name__ == "__main__":
    unittest.main()

