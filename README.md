# weather-based-activity-advisor
A Python service that recommends activities based on current city weather using Langchain and LLMs.

## Overview

This service:
1. Accepts a city name via an HTTP endpoint
2. Looks up current weather for that city (real API or mock)
3. Uses Langchain and an LLM to generate structured activity suggestions
4. Returns the suggestions in a well-defined JSON format

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/weather-activity-suggestions.git
cd weather-activity-suggestions

# Copy and edit the environment file
cp .env.example .env

# Edit .env with your API keys
OPENAI_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

## Running the Service

### Way 1: Quick Start with Docker

The easiest way to run the service is with Docker:

```bash
# Start the service with Docker Compose
docker-compose up -d
```

The API will be available at http://localhost:8000.

### Way 2: Without Docker 

If you prefer to run the service without Docker:



```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the service
uvicorn app.main:app --reload --port 8000
or 
fastapi run app/main.py --reload
```
The API will be available at http://localhost:8000.
## API Usage

### Get Activity Suggestions

```
POST /api/v1/activities
```

## Sample Requests

### Using curl

```bash
# request with a city name
curl -X POST http://localhost:8000/api/v1/activities \
  -H "Content-Type: application/json" \
  -d '{"city": "London"}'
```

**Example Response:**

```json
{
  "city": "london",
  "weather": {
    "temperature": 39,
    "conditions": "Clear",
    "humidity": 85,
    "wind_speed": 5
  },
  "activities": [
    {
      "name": "Visit the British Museum",
      "description": "Explore the vast collection of art and antiquities from around the world at the British Museum. It's a perfect indoor activity to stay warm and get culturally enriched.",
      "category": "Cultural"
    },
    {
      "name": "Afternoon Tea Experience",
      "description": "Enjoy a quintessential British afternoon tea at one of London's historic hotels or tea rooms. A cozy way to spend an afternoon indoors.",
      "category": "Food & Drink"
    },
    {
      "name": "Stroll Through Hyde Park",
      "description": "Bundle up for a leisurely walk in Hyde Park. The clear weather is ideal for enjoying the serene beauty of one of London's largest parks.",
      "category": "Entertainment"
    }
  ]
}
```

## Prompt Engineering Approach

The prompt engineering for this service was designed to achieve structured, relevant activity suggestions. Key aspects of the prompt design:

1. **System Context**: The prompt establishes the LLM as an "expert travel and activities consultant" to prime it for high-quality recommendations.

2. **Structure Definition**: The prompt explicitly defines the required fields for each activity:
   - name: Short, descriptive name
   - description: Brief explanation of what the activity involves
   - category: Classification of the activity type
   - 
3. **Injected Format Instructions**: The parser's format instructions are dynamically inserted into the prompt template as {format_instructions}. 
   
4. **Weather Context**: Complete weather details (temperature, conditions, humidity, wind speed) are provided to generate weather-appropriate suggestions.

5. **Output Schema**: Using Langchain's structured output parsers to ensure consistent JSON formatting.


```
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
```