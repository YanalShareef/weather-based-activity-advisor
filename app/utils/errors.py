class WeatherApiError(Exception):
    """Exception raised for errors related to the weather API."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LLMError(Exception):
    """Exception raised for errors related to the LLM service."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
