import logging
from itertools import product
from typing import List, Optional

from fastapi_cache.decorator import cache

from app import config
from app.exceptions import AirportDataException, APIRequestException
from app.models.flight_model import FlightResponseModel
from app.utils.utils import make_api_request

logger = logging.getLogger(__name__)

HEADERS = {
    "apikey": config.API_KEY,
    "User-Agent": config.USER_AGENT,
    "Accept": "application/json",
}


@cache(expire=3600)
async def get_cheapest_flights(
    source_airports: List[str], destination_airports: List[str], departure_date: str
) -> List[FlightResponseModel]:
    """
    Get the cheapest flights between source and destination airports.

    Args:
        source_airports (List[str]): List of source airports.
        destination_airports (List[str]): List of destination airports.
        departure_date (str): The departure date.

    Returns:
        List[FlightResponseModel]: List of flight data.
    """

    try:
        airport_combinations = product(source_airports, destination_airports)

        cheapest_flights = []
        for source, destination in airport_combinations:
            cheapest_flight = await fetch_cheapest_flight(
                source, destination, departure_date
            )

            if cheapest_flight:
                cheapest_flights.append(cheapest_flight)

        return cheapest_flights

    except Exception as e:
        logger.error(f"Failed to fetch cheapest flights: {e}")
        raise


@cache(expire=3600)
async def fetch_cheapest_flight(
    source_country: str, destination_country: str, departure_date: str
) -> Optional[FlightResponseModel]:
    """
    Service to return the cheapest flight.

    Args:
        source_country (str): Source country ISO code.
        destination_country (str): Destination country ISO code.
        departure_date (str): Date of departure in DD-MM-YYYY format.

    Returns:
        FlightResponseModel: List of flight data.
    """

    params = {
        "fly_from": source_country,
        "fly_to": destination_country,
        "date_from": departure_date,
        "date_to": departure_date,
        "sort": "price",
        "limit": 1,
    }

    try:
        flight_data = await make_api_request(config.SEARCH_API_URL, HEADERS, params)

        if flight_data:
            flights = flight_data.get("data", [])
            if flights:
                cheapest_flight = min(flights, key=lambda x: x["price"])
                return FlightResponseModel(
                    src=cheapest_flight["flyFrom"],
                    dst=cheapest_flight["flyTo"],
                    price=str(cheapest_flight["price"]),
                )
        else:
            raise APIRequestException(
                f"API returned no data for {source_country} to {destination_country} on {departure_date}"
            )

    except Exception as e:
        logger.error(f"Error fetching flight: {e}")
        raise


@cache(expire=86400)
async def fetch_top_3_airports(country: str) -> List[str]:
    """
    Service to return the top 3 airports by popularity for a given country.

    Args:
        country (str): Country ISO code.

    Returns:
        List[str]: A list of top 3 airport codes.
    """

    params = {
        "term": country,
        "location_types": "airport",
        "sort": "-dst_popularity_score",
        "limit": 3,
    }

    try:

        location_data = await make_api_request(config.LOCATION_API_URL, HEADERS, params)

        if location_data:
            locations = location_data.get("locations", [])
            if locations:
                return [location.get("code", "") for location in locations]
            else:
                raise AirportDataException(
                    f"No airport data found for country: {country}"
                )
        else:
            raise APIRequestException(
                f"No data received from the API for country: {country}"
            )

    except Exception as e:
        logger.error(f"Error fetching top airports: {e}")
        raise
