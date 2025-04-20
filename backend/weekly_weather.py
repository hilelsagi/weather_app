from backend.daily_weather import DailyWeather

class WeeklyWeather:
    """
    Represents the weekly weather report.

    Attributes:
        dailys (list): A list of seven DailyWeather objects.
        city (str): The city name.
        country (str): The country name.
    """

    def __init__(self):
        """
        Initializes a WeeklyWeather object with seven DailyWeather instances.
        """
        self.dailys = [DailyWeather() for _ in range(7)]
        self.city = ""
        self.country = ""

    def send_data_to_days(self, weekly_temperatures: list, weekly_humidity: list, weekly_times: list, city: str, country: str) -> None:
        """
        Processes parsed weekly data and distributes it to the DailyWeather objects.

        Args:
            weekly_temperatures (list): A list of temperature values for the week.
            weekly_humidity (list): A list of humidity values for the week.
            weekly_times (list): A list of timestamps for the week.
            city (str): The name of the city.
            country (str): The name of the country.

        Raises:
            ValueError: If any input list is empty or has insufficient data.
        """
        if not all(isinstance(lst, list) and lst for lst in [weekly_temperatures, weekly_humidity, weekly_times]):
            raise ValueError("Invalid or empty weather data lists provided.")

        if len(weekly_temperatures) < 168 or len(weekly_humidity) < 168 or len(weekly_times) < 168:
            raise ValueError("Insufficient weather data. Expected at least 168 values (24 per day for 7 days).")

        self.city = city
        self.country = country

        for d in self.dailys:
            # Extract 24-hour segments for each day's weather
            daily_times = weekly_times[:24]
            weekly_times = weekly_times[24:]
            daily_temperatures = weekly_temperatures[:24]
            weekly_temperatures = weekly_temperatures[24:]
            daily_humidity = weekly_humidity[:24]
            weekly_humidity = weekly_humidity[24:]

            d.set_attributes(daily_times, daily_temperatures, daily_humidity)

    def __str__(self) -> str:
        """
        Returns a string representation of the weekly weather forecast.

        Returns:
            str: Formatted weather summary for the week.
        """
        return "\n".join(str(d) for d in self.dailys)

