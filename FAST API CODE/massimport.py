#import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

#host = os.environ["POSTGRES_HOST"]
#port = os.environ["POSTGRES_PORT"]
#user = os.environ["POSTGRES_USER"]
#password = os.environ["POSTGRES_PASS"]
#db = os.environ["POSTGRES_DB"]
dbtype = "sqlite"

SQLALCHEMY_DATABASE_URI = f"{dbtype}:///farmgate.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# TODO: Add code to mass import all pdf files from a particular folder
