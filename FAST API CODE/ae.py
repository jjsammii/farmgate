import pdfplumber
from fastapi import Depends, File, UploadFile

from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from datetime import date
from crud import create_farmgateprice_entry, get_farmgateprices_by_parish_commodity
from models import FarmGatePrice
from database import SessionLocal, engine
from schemas import FarmGatePriceCreate
import os

# from sqlalchemy import creat_engine

# Get date for farmgate prices by extracting from the filename. Returns a date object


def getfiledate(filename: str):
    file_date = filename.split(sep=" ")
    date_comp = file_date[1].split(sep=".")
    return date(int(date_comp[2]), int(
        date_comp[0]), int(date_comp[1]))


def import_pdf(uploadedfile: File, filename: str, session: Session):

    # COLUMNS = [
    #     "parish",
    #     "price_date",
    #     "commodity",
    #     "source",
    #     "low",
    #     "high",
    #     "most_frequent",
    #     "supply",
    #     "grade"
    # ]

    table_settings = {
        "vertical_strategy": "lines",
        "intersection_x_tolerance": 15,
        "explicit_vertical_lines": [18, 597]
    }

    try:
        openpdf = pdfplumber.open(uploadedfile)
    except:
        return "Could not open "+filename+" as pdf"

    with openpdf as pdf:

        curr_price_date = getfiledate(filename)
        print("Processing " + filename)

        if session.query(FarmGatePrice).filter(FarmGatePrice.price_date == curr_price_date).first():
            return "Data already imported"
        else:
            totalpages = len(pdf.pages)
            for i in range(0, totalpages):

                curr_page = pdf.pages[i]
                #print("Processing page:", curr_page)
                table = curr_page.extract_table(table_settings)

                parish_row = table[0]
                if parish_row:
                    parish1 = parish_row[2].strip().replace("St.", "Saint")
                    parish2 = parish_row[7].strip().replace("St.", "Saint")

                    #curr_price_date = date(2021, 9, 4)

                    for row in table[3:-1]:
                        # Blank entries in the PDF have a dash, let's replace these with 0
                        # for index in range(0, 11):
                        #    row[index] = row[index].replace("-", "0")

                        if parish1:
                            if row[2] != "-":
                                # print(parish1, curr_price_date,
                                #      row[0], row[1], row[2], row[3], row[4], row[5], row[6])

                                new_farmgateprice = FarmGatePriceCreate(parish=parish1, price_date=curr_price_date, commodity=row[0].lower(), source=row[1], low=float(
                                    row[2]), high=float(row[3]), most_frequent=float(row[4]), supply=row[5], grade=row[6])
                                create_farmgateprice_entry(
                                    session=session, farmgateprice=new_farmgateprice)

                        if parish2:
                            if row[7] != "-":
                                # print(parish2, curr_price_date,
                                #      row[0], row[1], row[7], row[8], row[9], row[10], row[11])

                                new_farmgateprice = FarmGatePriceCreate(parish=parish2, price_date=curr_price_date, commodity=row[0].lower(), source=row[1], low=float(
                                    row[7]), high=float(row[8]), most_frequent=float(row[9]), supply=row[10], grade=row[11])
                                create_farmgateprice_entry(
                                    session=session, farmgateprice=new_farmgateprice)
                        #    print(parish2, row[0], row[1], row[7],
                        #         row[8], row[9], row[10], row[11])

        # im = p1.to_image()

        # table = p1.extract_table(table_settings)

        # parish_row = table[0]
        # parish1 = parish_row[2].strip()
        # parish2 = parish_row[7].strip()

        # im.reset().debug_tablefinder(table_settings)
        # im.save("./my1.png", format="PNG")

        return "Data imported"
