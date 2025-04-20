import requests

class APIHandler:
    """
    Handles API requests for city geolocation and weather data.
    """

    def send_city_request(self, city: str):
        """
        Sends a GET request to Open-Meteo's geolocation API to fetch geographical data for a given city.

        Args:
            city (str): The name of the city.

        Returns:
            requests.Response: The raw response object from the API.

        Raises:
            ValueError: If the city name is empty or invalid.
            ConnectionError: If the API request fails due to network issues.
            RuntimeError: If an unexpected error occurs.
        """
        if not city or not isinstance(city, str):
            raise ValueError("City name must be a non-empty string.")

        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
            return response

        except requests.exceptions.Timeout:
            raise ConnectionError("City API request timed out. Please try again.")
        except requests.exceptions.RequestException as req_err:
            raise ConnectionError(f"City API request failed: {req_err}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in send_city_request: {e}")

    def send_weather_request(self, coords: tuple):
        """
        Sends a GET request to Open-Meteo's weather API to retrieve weekly weather data.

        Args:
            coords (tuple): A tuple containing (latitude, longitude) of the city.

        Returns:
            requests.Response: The raw response object from the API.

        Raises:
            ValueError: If coordinates are missing or invalid.
            ConnectionError: If the API request fails due to network issues.
            RuntimeError: If an unexpected error occurs.
        """
        if not coords or len(coords) != 2:
            raise ValueError("Invalid coordinates provided. Expected (latitude, longitude).")

        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&hourly=temperature_2m,relative_humidity_2m&forecast_days=7"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            raise ConnectionError("Weather API request timed out. Please try again.")
        except requests.exceptions.RequestException as req_err:
            raise ConnectionError(f"Weather API request failed: {req_err}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in send_weather_request: {e}")

