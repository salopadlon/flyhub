from pydantic import BaseModel


class FlightResponseModel(BaseModel):
    """
    Flight Response Model

    Attributes:
        src: str
            Source country code.
        dst: str
            Destination country code.
        price: str
            Price of the flight.
    """

    src: str
    dst: str
    price: str
