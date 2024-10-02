import logging
from datetime import datetime
from typing import List, Optional, Union

import httpx

from app.exceptions import FlightSortingException
from app.models.flight_model import FlightResponseModel

logger = logging.getLogger(__name__)


def sort_flights_by_price(
    flights: List[Union[FlightResponseModel, dict]]
) -> List[FlightResponseModel]:
    """
    Sort the flights by price.

    Args:
        flights (List[FlightResponseModel]): List of flight data.

    Returns:
        List[FlightResponseModel]: Sorted list of flight data
    """

    if not flights:
        return []

    try:
        # Ensure all flights are instances of FlightResponseModel
        flight_objects = [
            (
                flight
                if isinstance(flight, FlightResponseModel)
                else FlightResponseModel(**flight)
            )
            for flight in flights
        ]

        return sorted(flight_objects, key=lambda flight: int(flight.price))

    except (TypeError, ValueError) as e:
        logger.error(f"Error occurred while sorting flights: {e}", exc_info=True)
        raise FlightSortingException("Error occurred while sorting flights")


async def make_api_request(url: str, headers: dict, params: dict) -> Optional[dict]:
    """
    Helper function to make async API requests.

    Args:
        url (str): The API URL.
        headers (dict): The headers for the request.
        params (dict): The query parameters.

    Returns:
        Optional[dict]: The response JSON data if successful, otherwise None.
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(
                f"API request to {url} succeeded with status {response.status_code}"
            )
            return response.json()

        except httpx.RequestError as exc:
            logger.error(
                f"An error occurred while requesting {exc.request.url!r}: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc}"
            )
        except Exception as exc:
            logger.error(f"An unexpected error occurred: {exc}")

    return None


def is_date_valid(departure_date: str) -> bool:
    """
    Validates that the departure date follows the DD/MM/YYYY format.

    Args:
        departure_date (str): The departure date string.

    Returns:
        bool: True if the date is valid, False otherwise.
    """

    try:
        datetime.strptime(departure_date, "%d/%m/%Y")
        return True
    except ValueError:
        return False
