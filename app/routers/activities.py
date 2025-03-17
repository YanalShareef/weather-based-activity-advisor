from fastapi import APIRouter, HTTPException, Depends
from app.models.request import CityRequest
from app.models.response import ActivityResponse, ErrorResponse
from app.services.weather import WeatherService
from app.services.llm import LLMService
from app.utils.errors import WeatherApiError, LLMError


# Create router
router = APIRouter(prefix="/api/v1", tags=["activities"])


# Dependency for weather service
def get_weather_service():
    return WeatherService()


# Dependency for LLM service
def get_llm_service():
    return LLMService()


@router.post(
    "/activities",
    response_model=ActivityResponse,
    responses={
        200: {
            "model": ActivityResponse,
            "description": "Successfully retrieved activity suggestions",
        },
        404: {"model": ErrorResponse, "description": "City not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_activity_suggestions(
    request: CityRequest,
    weather_service: WeatherService = Depends(get_weather_service),
    llm_service: LLMService = Depends(get_llm_service),
):
    """
    Get activity suggestions based on the current weather in a city.

    Args:
        request: Request containing the city name
        weather_service: Service to get weather data
        llm_service: Service to generate activity suggestions

    Returns:
        JSON response with city, weather, and activity suggestions

    Raises:
        HTTPException: If there's an error getting weather data or generating suggestions
    """
    try:
        # Get weather data for the requested city
        weather_data = weather_service.get_weather(request.city)

        # Generate activity suggestions
        result = llm_service.generate_activities(request.city, weather_data)

        return result

    except WeatherApiError as e:
        status_code = getattr(e, "status_code", 500)
        raise HTTPException(status_code=status_code, detail=str(e))

    except LLMError as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating activity suggestions: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
