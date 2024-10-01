import pytest

from app.exceptions import FlightSortingException
from app.models.flight_model import FlightResponseModel
from app.utils.utils import sort_flights_by_price


def test_sort_flights_by_price_success():
    # GIVEN
    flights = [
        FlightResponseModel(src="JFK", dst="LAX", price="300"),
        FlightResponseModel(src="SFO", dst="SEA", price="200"),
        FlightResponseModel(src="ORD", dst="MIA", price="100"),
    ]

    # WHEN
    sorted_flights = sort_flights_by_price(flights)

    # THEN
    assert sorted_flights[0].price == "100"
    assert sorted_flights[1].price == "200"
    assert sorted_flights[2].price == "300"


def test_sort_flights_by_price_empty():
    # GIVEN
    flights = []

    # WHEN
    sorted_flights = sort_flights_by_price(flights)

    # THEN
    assert sorted_flights == []


def test_sort_flights_by_price_invalid_data():
    # GIVEN
    flights = [
        {"src": "JFK", "dst": "LAX", "price": "300"},
        {"src": "SFO", "dst": "SEA", "price": None},
    ]

    # THEN
    with pytest.raises(FlightSortingException):
        sort_flights_by_price(flights)
