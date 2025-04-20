import json

class CityParser:
    """
    This class represents a data parser that processes JSON responses 
    from the Open-Meteo API and extracts city-related data.

    Attributes:
        __coords (tuple): A tuple containing (latitude, longitude).
        __city (str): The city name.
        __country (str): The country name.
    """

    def __init__(self):
        """
        Initializes city-related attributes.
        """
        self.__coords = None
        self.__city = ""
        self.__country = ""

    def set_attributes(self, json_data) -> None:
        """
        Parses and stores city-related data from a JSON response.

        Args:
            json_data (str): A JSON string containing city location data.

        Raises:
            ValueError: If the JSON data is missing required keys or is invalid.
            json.JSONDecodeError: If the JSON format is incorrect.
        """
        try:
            data = json.loads(json_data)

            # Validate that the response contains the expected structure
            if "results" not in data or not isinstance(data["results"], list) or len(data["results"]) == 0:
                raise ValueError("Invalid city data: No results found.")

            city_info = data["results"][0]

            # Ensure all required fields exist
            if not all(k in city_info for k in ["name", "latitude", "longitude", "country"]):
                raise ValueError("Missing required city data fields.")

            self.__city = city_info["name"]
            self.__coords = (city_info["latitude"], city_info["longitude"])
            self.__country = city_info["country"]

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format received in city data.")
        except ValueError:
            raise #Passing valueError and not reraising RuntimeError
        except Exception as e:
            raise RuntimeError(f"Unexpected error while parsing city data: {e}")

    def get_country(self) -> str:
        """
        Returns the country name.

        Returns:
            str: The country name.
        """
        return self.__country

    def get_coords(self) -> tuple:
        """
        Returns the coordinates (latitude, longitude) of the city.

        Returns:
            tuple: A tuple containing (latitude, longitude).
        """
        return self.__coords

    def get_city(self) -> str:
        """
        Returns the city name.

        Returns:
            str: The city name.
        """
        return self.__city

