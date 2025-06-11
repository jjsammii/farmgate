from datetime import date
from pydantic import BaseModel


class FarmGatePriceBase(BaseModel):
    #    farmgatepriceId: int
    parish: str
    price_date: date
    commodity: str
    source: str
    low: float
    high: float
    most_frequent: float
    supply: str
    grade: str


class FarmGatePriceCreate(FarmGatePriceBase):
    pass


class FarmGatePrice(FarmGatePriceBase):
    farmgatepriceId: int
