from schemas import FarmGatePriceBase, FarmGatePriceCreate
from datetime import date
from typing import List

from sqlalchemy.orm import Session
from models import FarmGatePrice


def get_farmgateprices_by_date(session: Session, year: int, month: int, day: int) -> FarmGatePrice:
    query_date = date(year, month, day)
    return session.query(FarmGatePrice).filter(FarmGatePrice.price_date == query_date).all()


def get_farmgateprices_by_parish_commodity(session: Session, parish: str, commodity: str) -> FarmGatePrice:
    return session.query(FarmGatePrice).filter(FarmGatePrice.commodity == commodity, FarmGatePrice.parish == parish).all()


def get_farmgateprices_by_parish_commodity_date(session: Session, parish: str, commodity: str, year: int, month: int, day: int) -> FarmGatePrice:
    query_date = date(year, month, day)
    return session.query(FarmGatePrice).filter(FarmGatePrice.commodity == commodity, FarmGatePrice.parish == parish, FarmGatePrice.price_date == query_date).all()


def get_farmgateprices_by_commodity(session: Session, commodity: str) -> FarmGatePrice:
    return session.query(FarmGatePrice).filter(FarmGatePrice.commodity == commodity).all()


def get_farmgateprices(session: Session, skip: int = 0, limit: int = 100) -> List[FarmGatePrice]:
    return session.query(FarmGatePrice).offset(skip).limit(limit).all()
  # print(session.query(FarmGatePrice).all())
  # return session.query(FarmGatePrice).all()


def create_farmgateprice_entry(session: Session, farmgateprice: FarmGatePriceCreate):
    new_farmgateprice = FarmGatePrice(parish=farmgateprice.parish, price_date=farmgateprice.price_date, commodity=farmgateprice.commodity, source=farmgateprice.source,
                                      low=farmgateprice.low, high=farmgateprice.high, most_frequent=farmgateprice.most_frequent, supply=farmgateprice.supply, grade=farmgateprice.grade)
    session.add(new_farmgateprice)
    session.commit()
    session.refresh(new_farmgateprice)
    return new_farmgateprice


# parish: str, price_date: date, commodity: str, source: str, low: float, high: float, most_frequent: float, supply: str, grade: str) -> FarmGatePriceCreate:
#  parish: str
#     price_date: date
#     commodity: str
#     source: str
#     low: float
#     high: float
#     most_frequent: float
#     supply: str
#     grade: str
