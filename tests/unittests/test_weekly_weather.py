import unittest
from backend.weekly_weather import WeeklyWeather
from backend.daily_weather import DailyWeather

class TestWeeklyWeather(unittest.TestCase):

    def setUp(self):
        """Initialize WeeklyWeather before each test."""
        self.weekly_weather = WeeklyWeather()

    def test_send_data_to_days_valid(self):
        """Test setting attributes with valid weekly data."""
        city = "Paris"
        country = "France"

        # Generate test data for 7 days (24 hours each)
        weekly_times = [f"2025-02-{8 + i//24}T{(i % 24):02d}:00" for i in range(168)]
        weekly_temperatures = [i % 15 + 5.0 for i in range(168)]
        weekly_humidity = [60 + (i % 5) for i in range(168)]

        self.weekly_weather.send_data_to_days(weekly_temperatures, weekly_humidity, weekly_times, city, country)

        self.assertEqual(self.weekly_weather.city, "Paris")
        self.assertEqual(self.weekly_weather.country, "France")
        self.assertEqual(len(self.weekly_weather.dailys), 7)

        # Check one day's data
        first_day = self.weekly_weather.dailys[0]
        self.assertEqual(first_day.get_date(), "08-02-2025")
        self.assertEqual(first_day.get_name(), "Saturday")
        self.assertEqual(first_day.get_night(), 5.0)  # Min temp of first 24 values
        self.assertEqual(first_day.get_day(), 19.0)  # Max temp of first 24 values
        self.assertAlmostEqual(first_day.get_humidity(), 62.0, delta=0.5)  # Avg humidity

    def test_send_data_to_days_insufficient_data(self):
        """Test handling of insufficient weather data (< 168 values)."""
        city = "Paris"
        country = "France"

        weekly_times = [f"2025-02-08T{hour:02d}:00" for hour in range(120)]  # Only 5 days
        weekly_temperatures = [i % 15 + 5.0 for i in range(120)]
        weekly_humidity = [60 + (i % 5) for i in range(120)]

        with self.assertRaises(ValueError) as cm:
            self.weekly_weather.send_data_to_days(weekly_temperatures, weekly_humidity, weekly_times, city, country)

        self.assertIn("Insufficient weather data", str(cm.exception))

    def test_send_data_to_days_empty_lists(self):
        """Test handling of empty lists."""
        with self.assertRaises(ValueError) as cm:
            self.weekly_weather.send_data_to_days([], [60]*168, [f"2025-02-08T{hour:02d}:00" for hour in range(168)], "Paris", "France")
        self.assertIn("Invalid or empty weather data lists provided.", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            self.weekly_weather.send_data_to_days([10.0]*168, [], [f"2025-02-08T{hour:02d}:00" for hour in range(168)], "Paris", "France")
        self.assertIn("Invalid or empty weather data lists provided.", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            self.weekly_weather.send_data_to_days([10.0]*168, [60]*168, [], "Paris", "France")
        self.assertIn("Invalid or empty weather data lists provided.", str(cm.exception))

    def test_str_representation(self):
        """Test string representation of weekly weather."""
        city = "Paris"
        country = "France"
        weekly_times = [f"2025-02-{8 + i//24}T{(i % 24):02d}:00" for i in range(168)]
        weekly_temperatures = [i % 15 + 5.0 for i in range(168)]
        weekly_humidity = [60 + (i % 5) for i in range(168)]

        self.weekly_weather.send_data_to_days(weekly_temperatures, weekly_humidity, weekly_times, city, country)

        weekly_summary = str(self.weekly_weather)
        self.assertIn("Saturday, 08-02-2025", weekly_summary)
        self.assertIn("Sunday, 09-02-2025", weekly_summary)
        self.assertIn("Friday, 14-02-2025", weekly_summary)

if __name__ == "__main__":
    unittest.main()

