class FlightSortingException(Exception):
    """Custom exception raised when an error occurs during flight sorting."""

    def __init__(self, message: str):
        super().__init__(message)


class FlightServiceException(Exception):
    """Base class for exceptions in the flight service."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class APIRequestException(FlightServiceException):
    """Exception raised when an error occurs during an API request."""

    def __init__(self, message="An error occurred while making an API request"):
        super().__init__(message)


class AirportDataException(FlightServiceException):
    """Exception raised when no airport data is found for a given country."""

    def __init__(self, message="No airport data found for the given country"):
        super().__init__(message)
