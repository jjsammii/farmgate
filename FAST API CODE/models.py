from typing import TypedDict
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date

from database import Base


class FarmgatePriceDict(TypedDict):
    farmgatepriceId: int
    parish: str
    price_date: date
    commodity: str
    source: str
    low: float
    high: float
    most_frequent: float
    supply: str
    grade: str


class FarmGatePrice(Base):
    """
    Define the farmgate price model
    """

    __tablename__ = "farmgateprice"

    farmgatepriceId = Column(Integer, autoincrement=True, primary_key=True)
    parish = Column(String)
    commodity = Column(String)
    price_date = Column(Date)
    source = Column(String)
    low = Column(Float)
    high = Column(Float)
    most_frequent = Column(Float)
    supply = Column(String)
    grade = Column(String)

    def __init__(self, parish: str, price_date: date, commodity: str, source: str, low: float, high: float, most_frequent: float, supply: str, grade: str):
        self.parish = parish
        self.price_date = price_date
        self.commodity = commodity
        self.source = source
        self.low = low
        self.high = high
        self.most_frequent = most_frequent
        self.supply = supply
        self.grade = grade

    def __repr__(self) -> str:
        return f"<FarmgatePrice {self.farmgatepriceId}>"

    @property
    def serialize(self) -> FarmgatePriceDict:
        """
        Return item in serializeable format
        """
        return {"farmgatepriceId": self.farmgatepriceId, "parish": self.parish, "price_date": self.price_date, "commodity": self.commodity, "source": self.source, "low": self.low, "high": self.high, "most_frequent": self.most_frequent, "supply": self.supply, "grade": self.grade}
       # return("great")
