import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Weather-Based Activity Recommender",
    description="A service that suggests activities based on the current weather in a city",
    version="0.1.0",
)


@app.get("/")
async def root():
    """Root endpoint that returns basic service information."""
    return {
        "service": "Weather-Based Activity Recommender",
        "status": "operational",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=debug)
