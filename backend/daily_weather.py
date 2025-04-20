from datetime import datetime

class DailyWeather:
    """
    Represents the daily weather forecast.
    
    All temperature values are in Celsius, and humidities are in percentages.
    
    Attributes:
        date (str): The formatted date of the forecast.
        humidity (float): The average humidity for the day.
        night (float): The lowest temperature recorded at night.
        day (float): The highest temperature recorded during the day.
        name (str): The name of the day (e.g., Monday, Tuesday).
    """

    def __init__(self):
        """
        Initializes daily weather attributes with default values.
        """
        self.date = ""
        self.humidity = 0.0
        self.night = 0.0
        self.day = 0.0
        self.name = ""

    def get_date(self) -> str:
        """
        Returns the date of the forecast.

        Returns:
            str: Formatted date as 'DD-MM-YYYY'.
        """
        return self.date

    def get_night(self) -> float:
        """
        Returns the minimum nighttime temperature.

        Returns:
            float: Nighttime temperature in Celsius.
        """
        return self.night

    def get_day(self) -> float:
        """
        Returns the maximum daytime temperature.

        Returns:
            float: Daytime temperature in Celsius.
        """
        return self.day

    def get_humidity(self) -> float:
        """
        Returns the average humidity for the day.

        Returns:
            float: Humidity percentage.
        """
        return self.humidity

    def get_name(self) -> str:
        """
        Returns the name of the day.

        Returns:
            str: Name of the day (e.g., Monday).
        """
        return self.name

    def set_attributes(self, times: list, temperatures: list, humidities: list) -> None:
        """
        Sets daily weather attributes using provided lists of times, temperatures, and humidity values.

        Args:
            times (list): List of timestamps in 'YYYY-MM-DDTHH:MM' format.
            temperatures (list): List of temperature values in Celsius.
            humidities (list): List of humidity percentage values.

        Raises:
            ValueError: If any list is empty or contains invalid data.
        """
        if not times or not isinstance(times, list):
            raise ValueError("Invalid or empty 'times' list provided.")
        if not temperatures or not isinstance(temperatures, list):
            raise ValueError("Invalid or empty 'temperatures' list provided.")
        if not humidities or not isinstance(humidities, list):
            raise ValueError("Invalid or empty 'humidities' list provided.")

        try:
            api_style_date = times[0].split("T")[0]
            date_obj = datetime.strptime(api_style_date, "%Y-%m-%d")
            self.date = date_obj.strftime("%d-%m-%Y")
            self.name = date_obj.strftime("%A")

            self.humidity = round(sum(humidities) / len(humidities), 2)
            self.day = max(temperatures)
            self.night = min(temperatures)

        except IndexError:
            raise ValueError("Error extracting date: 'times' list is empty or malformed.")
        except ValueError as ve:
            raise ValueError(f"Error processing weather data: {ve}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while setting daily weather attributes: {e}")

    def __str__(self) -> str:
        """
        Returns a string representation of the daily weather forecast.

        Returns:
            str: Formatted weather summary for the day.
        """
        return f"{self.name}, {self.date}: Day: {self.day}°C, Night: {self.night}°C, Humidity: {self.humidity}%"

