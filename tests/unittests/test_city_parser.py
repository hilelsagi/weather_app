import unittest
import json
from backend.city_parser import CityParser  # ✅ Absolute Import

class TestCityParser(unittest.TestCase):

    def setUp(self):
        """Initialize CityParser before each test."""
        self.parser = CityParser()

    def test_set_attributes_valid_json(self):
        """Test setting attributes with valid JSON data."""
        json_data = json.dumps({
            "results": [
                {"name": "Paris", "latitude": 48.8566, "longitude": 2.3522, "country": "France"}
            ]
        })

        self.parser.set_attributes(json_data)

        self.assertEqual(self.parser.get_city(), "Paris")
        self.assertEqual(self.parser.get_country(), "France")
        self.assertEqual(self.parser.get_coords(), (48.8566, 2.3522))

    def test_set_attributes_missing_fields(self):
        """Test missing required fields in JSON."""
        json_data = json.dumps({
            "results": [
                {"name": "Paris", "latitude": 48.8566, "country": "France"}  # Missing "longitude"
            ]
        })

        with self.assertRaises(ValueError) as cm:
            self.parser.set_attributes(json_data)

        self.assertIn("Missing required city data fields.", str(cm.exception))

    def test_set_attributes_empty_results(self):
        """Test JSON with empty 'results' array."""
        json_data = json.dumps({"results": []})

        with self.assertRaises(ValueError) as cm:
            self.parser.set_attributes(json_data)

        self.assertIn("Invalid city data: No results found.", str(cm.exception))

    def test_set_attributes_invalid_json(self):
        """Test invalid JSON format (raises JSONDecodeError)."""
        invalid_json = "{results: [ {name: Paris, latitude: 48.8566, longitude: 2.3522, country: France} ]}"

        with self.assertRaises(ValueError) as cm:
            self.parser.set_attributes(invalid_json)

        self.assertIn("Invalid JSON format received in city data.", str(cm.exception))

    def test_get_city_before_setting(self):
        """Test default city before setting attributes."""
        self.assertEqual(self.parser.get_city(), "")

    def test_get_country_before_setting(self):
        """Test default country before setting attributes."""
        self.assertEqual(self.parser.get_country(), "")

    def test_get_coords_before_setting(self):
        """Test default coordinates before setting attributes (should be None)."""
        self.assertIsNone(self.parser.get_coords())

if __name__ == "__main__":
    unittest.main()

