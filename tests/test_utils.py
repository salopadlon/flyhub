import pytest

from app.exceptions import FlightSortingException
from app.models.flight_model import FlightResponseModel
from app.utils.utils import is_date_valid, sort_flights_by_price


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


def test_is_date_valid_with_valid_date():
    # GIVEN
    valid_date = "15/10/2023"

    # THEN
    assert is_date_valid(valid_date) == True


def test_is_date_valid_with_invalid_date_format():
    # GIVEN
    invalid_date = "10/15/2023"

    # THEN
    assert is_date_valid(invalid_date) == False


def test_is_date_valid_with_invalid_day():
    # GIVEN
    invalid_day = "31/02/2023"

    # THEN
    assert is_date_valid(invalid_day) == False


def test_is_date_valid_with_empty_string():
    # GIVEN
    empty_date = ""

    # THEN
    assert is_date_valid(empty_date) == False


def test_is_date_valid_with_invalid_characters():
    # GIVEN
    invalid_date = "abc/def/ghij"

    # THEN
    assert is_date_valid(invalid_date) == False
