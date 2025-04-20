import json

class WeatherParser:
    """
    This class represents a weather parser. It takes a JSON response from the Open-Meteo API
    and extracts weekly weather data.
    """

    def __init__(self):
        """
        Initializes empty lists to store weekly weather data.
        """
        self.__weekly_times = []
        self.__weekly_humidities = []
        self.__weekly_temperatures = []

    def parse_data(self, json_data) -> None:
        """
        Parses the JSON weather data and extracts relevant information.

        Args:
            json_data (str): A JSON string containing weather data from the API.

        Raises:
            ValueError: If the JSON data is invalid or missing required keys.
            json.JSONDecodeError: If the input is not valid JSON.
        """
        try:
            data = json.loads(json_data)

            # Validate necessary keys exist
            if "hourly" not in data:
                raise ValueError("Missing 'hourly' key in weather data.")
            if not all(key in data["hourly"] for key in ["time", "temperature_2m", "relative_humidity_2m"]):
                raise ValueError("Incomplete weather data received.")

            self.__weekly_times = data["hourly"]["time"]
            self.__weekly_temperatures = data["hourly"]["temperature_2m"]
            self.__weekly_humidities = data["hourly"]["relative_humidity_2m"]

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format received in weather data.")
        except ValueError:
            raise #Passing ValueError instead of reraising RuntimeError
        except Exception as e:
            raise RuntimeError(f"Unexpected error while parsing weather data: {e}")

    def get_weekly_times(self) -> list:
        """
        Returns the list of timestamps for the weekly forecast.

        Returns:
            list: A list of timestamps in ISO format.
        """
        return self.__weekly_times

    def get_weekly_temperatures(self) -> list:
        """
        Returns the list of weekly temperatures.

        Returns:
            list: A list of temperatures in degrees Celsius.
        """
        return self.__weekly_temperatures

    def get_weekly_humidities(self) -> list:
        """
        Returns the list of weekly relative humidity values.

        Returns:
            list: A list of humidity percentages.
        """
        return self.__weekly_humidities

