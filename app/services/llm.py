import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

from ..models.response import ActivityResponse
from ..utils.errors import LLMError
from typing import Dict, Any

# Load environment variables
load_dotenv()


class LLMService:
    """Service to generate activity suggestions using Langchain and LLMs."""

    def __init__(self):
        """
        Initialize the LLM service.

        """
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise LLMError("OpenAI API key not configured")

        # Initialize the LLM
        self.llm = ChatOpenAI(
            api_key=self.api_key, model="gpt-4-turbo-preview", temperature=0.7
        )

        # Create the output parser and prompt template
        self.output_parser = JsonOutputParser(pydantic_object= ActivityResponse)
        self.prompt_template = self._create_prompt_template()

        # Build the chain
        self.chain = self._build_chain()


    def _create_prompt_template(self):
        """Create the prompt template for activity generation."""

        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
            You are an expert travel and activities consultant. Your task is to suggest suitable activities
            based on the current weather conditions in a city. Focus on activities that make sense given
            the current weather.

            For each activity, include the following information:
            - name: A short, descriptive name for the activity
            - description: A brief description of what the activity involves
            - category: The category the activity belongs to (e.g., 'Food & Drink', 'Cultural', 'Sports', 'Entertainment')

            Return up to 3 activities in the specified JSON format.

            {format_instructions}
            """,
                ),
                (
                    "human",
                    """
            City: {city}

            Weather:
            - Temperature: {temperature}°F
            - Conditions: {conditions}
            - Humidity: {humidity}%
            - Wind Speed: {wind_speed} mph

            Please suggest activities appropriate for these conditions.
            """,
                ),
            ]
        )

        return template

    def _build_chain(self):
        """Build the Langchain processing chain."""
        return (
            RunnablePassthrough()
            | self._prepare_input
            | self.prompt_template
            | self.llm
            | self.output_parser
        )

    def _prepare_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare the input data for the prompt template.

        Args:
            input_data: Input data including city and weather information

        Returns:
            Dict with formatted input for the prompt template
        """
        # Extract basic information
        city = input_data.get("city", "")
        weather = input_data.get("weather", {})

        # Prepare the formatted input
        return {
            "format_instructions": self.output_parser.get_format_instructions(),
            "city": city,
            "temperature": weather.get("temperature", 0),
            "conditions": weather.get("conditions", "Unknown"),
            "humidity": weather.get("humidity", 0),
            "wind_speed": weather.get("wind_speed", 0),
        }

    def generate_activities(
        self, city: str, weather_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate activity suggestions based on city and weather data.

        Args:
            city: Name of the city
            weather_data: Weather data including temperature, conditions, etc.

        Returns:
            Dictionary with city, weather, and activity suggestions

        Raises:
            LLMError: If there's an error generating suggestions
        """
        try:
            # Prepare the input for the chain
            chain_input = {"city": city, "weather": weather_data}

            # Execute the chain
            result = self.chain.invoke(chain_input)

            # Format the final response
            activities = result.get("activities", [])

            return {"city": city, "weather": weather_data, "activities": activities}

        except Exception as e:
            raise LLMError(f"Error generating activities: {str(e)}")
