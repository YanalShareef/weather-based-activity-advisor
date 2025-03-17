import requests
import os
from dotenv import load_dotenv
from app.utils.errors import WeatherApiError
from typing import Dict, Any

# Load environment variables
load_dotenv()


class WeatherService:
    """Service to fetch weather data for the requested city."""

    def __init__(self):

        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Get weather data for the requested city.

        Args:
            city (str): Name of the city to get weather for

        Returns:
            dict: Weather data including temperature, conditions, humidity, and wind speed

        Raises:
            WeatherApiError: If the API call fails or the city is not found
        """

        if not self.api_key:
            raise WeatherApiError("OpenWeatherMap API key not configured")

        params = {"q": city, "appid": self.api_key, "units": "imperial"}

        try:
            response = requests.get(self.base_url, params=params)

            # Handle city not found
            if response.status_code == 404:
                raise WeatherApiError(f"City not found: {city}", status_code=404)

            # Handle other API errors
            response.raise_for_status()

            data = response.json()

            # Extract relevant weather data
            weather_data = {
                "temperature": round(data["main"]["temp"]),
                "conditions": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"]),
            }

            return weather_data

        except requests.exceptions.RequestException as e:
            raise WeatherApiError(f"Weather API error: {str(e)}")
