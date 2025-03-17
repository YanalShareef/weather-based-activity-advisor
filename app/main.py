import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import activities

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Weather-Based Activity Recommender",
    description="A service that suggests activities based on the current weather in a city",
    version="0.1.0",
)

# Include routers
app.include_router(activities.router)


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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
