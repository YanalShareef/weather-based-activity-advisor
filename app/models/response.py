from pydantic import BaseModel, Field
from typing import List, Optional


class WeatherData(BaseModel):
    """Model for weather information."""

    temperature: float = Field(..., description="Temperature in Fahrenheit")
    conditions: str = Field(..., description="Weather conditions (e.g., Sunny, Rainy)")
    humidity: int = Field(..., description="Humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in mph")


class Activity(BaseModel):
    """Model for a single activity suggestion."""

    name: str = Field(..., description="Name of the activity")
    description: str = Field(..., description="Brief description of the activity")
    category: str = Field(
        ..., description="Category of the activity (e.g., 'Sports', 'Cultural')"
    )


class ActivityResponse(BaseModel):
    """Model for the complete response from the activity suggestion endpoint."""

    city: str = Field(..., description="Name of the city requested")
    weather: WeatherData = Field(
        ..., description="Current weather information for the city"
    )
    activities: List[Activity] = Field(..., description="List of suggested activities")


class ErrorResponse(BaseModel):
    """Model for API error responses."""

    detail: str = Field(..., description="Error description")
    error_code: Optional[str] = Field(
        None, description="Optional error code for categorizing errors"
    )
