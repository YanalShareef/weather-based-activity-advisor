from pydantic import BaseModel, Field


class CityRequest(BaseModel):
    """Model for the request payload when requesting activity suggestions."""

    city: str = Field(..., description="The name of the city to get activities for")
