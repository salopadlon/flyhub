import logging
from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.exceptions import FlightServiceException, FlightSortingException
from app.models.flight_model import FlightResponseModel
from app.services.flight_service import fetch_top_3_airports, get_cheapest_flights
from app.utils.utils import sort_flights_by_price

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/search-flights", response_model=List[FlightResponseModel])
async def search_flights(
    source_country: str = Query(..., description="Source country code"),
    destination_country: str = Query(..., description="Destination country code"),
    departure_date: str = Query(
        ..., description="Date of departure in DD-MM-YYYY format"
    ),
) -> List[FlightResponseModel]:
    """
    Search for flights based on source, destination, and departure date. Returns list of cheapest flights as all
    possible combinations with top 3 source and destination airports on selected date.

    Args:
        source_country (str): Source country ISO code.
        destination_country (str): Destination country ISO code.
        departure_date (str): Date of departure in DD-MM-YYYY format.

    Returns:
        List[FlightResponseModel]: List of flight data.
    """

    try:
        source_airports = await fetch_top_3_airports(source_country)
        destination_airports = await fetch_top_3_airports(destination_country)
        cheapest_flights = await get_cheapest_flights(
            source_airports, destination_airports, departure_date
        )
        return sort_flights_by_price(cheapest_flights)
    except FlightServiceException as e:
        logger.error(f"FlightServiceException: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except FlightSortingException as e:
        logger.error(f"FlightSortingException: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
