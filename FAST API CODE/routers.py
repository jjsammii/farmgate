from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.datastructures import UploadFile
#from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

import os
import ae
import crud
import models
from database import SessionLocal, engine
from schemas import FarmGatePriceBase


models.Base.metadata.create_all(bind=engine)
farmgatepricerouter = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@farmgatepricerouter.get("/farmgateprices/", response_model=List[FarmGatePriceBase])
def read_farmgateprices(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    farmgateprices = crud.get_farmgateprices(
        session=session, skip=skip, limit=limit)
    if farmgateprices is None:
        raise HTTPException(
            status_code=404, detail="Farmgate records not found - load the database first")
    return(i.serialize for i in farmgateprices)


@farmgatepricerouter.get("/farmgateprices/{year}/{month}/{day}/", response_model=List[FarmGatePriceBase])
def read_farmgateprice(month: int, year: int, day: int, session: Session = Depends(get_session)):
    farmgateprices = crud.get_farmgateprices_by_date(
        session=session, month=month, year=year, day=day)
    if farmgateprices is None:
        raise HTTPException(
            status_code=404, detail="Farmgate records not found")
    return(i.serialize for i in farmgateprices)


@farmgatepricerouter.get("/farmgateprices/{parish}/{commodity}/", response_model=List[FarmGatePriceBase])
def read_farmgateprice(parish: str, commodity: str, session: Session = Depends(get_session)):
    farmgateprices = crud.get_farmgateprices_by_parish_commodity(
        session=session, parish=parish, commodity=commodity)
    if farmgateprices is None:
        raise HTTPException(
            status_code=404, detail="Farmgate records not found")
    return(i.serialize for i in farmgateprices)


@farmgatepricerouter.get("/farmgateprices/{parish}/{commodity}/{year}/{month}/{day}/", response_model=List[FarmGatePriceBase])
def read_farmgateprice(parish: str, commodity: str, month: int, year: int, day: int, session: Session = Depends(get_session)):
    farmgateprices = crud.get_farmgateprices_by_parish_commodity_date(
        session=session, parish=parish, commodity=commodity, month=month, year=year, day=day)
    if farmgateprices is None:
        raise HTTPException(
            status_code=404, detail="Farmgate records not found")
    return(i.serialize for i in farmgateprices)


@farmgatepricerouter.get("/farmgateprices/commodity/{commodity}/", response_model=List[FarmGatePriceBase])
def read_farmgateprice(commodity: str, session: Session = Depends(get_session)):
    farmgateprices = crud.get_farmgateprices_by_commodity(
        session=session, commodity=commodity)
    if farmgateprices is None:
        raise HTTPException(
            status_code=404, detail="Farmgate records not found")
    return(i.serialize for i in farmgateprices)


@farmgatepricerouter.get("/admin/upload/")
def upload_file():
    content = """
    <body>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)


@farmgatepricerouter.post("/uploadfiles/")
async def create_upload_fies(files: List[UploadFile] = File(...), session: Session = Depends(get_session)):
    results = []
    for file in files:
        status = ae.import_pdf(file.file, file.filename, session)
        results.append([file.filename, status])

    return {"results": results}


@farmgatepricerouter.get("/import/local/")
async def massImport(session: Session = Depends(get_session)):
    results = []
    for file in os.listdir('./data'):
        if file.endswith('.pdf'):
            afile = file(file)
            status = ae.import_pdf(afile, file, session)
            results.append([file.filename, status])

    return {"results": results}
