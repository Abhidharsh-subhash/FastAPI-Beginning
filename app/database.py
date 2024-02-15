from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

# it is the database url format
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
password = 'abhidharsh@1999'
encoded_password = urllib.parse.quote_plus(password)
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{encoded_password}@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# we ge a session to our database and everytime we got a request we get a session and after the request is done then close it out.
# we can keep calling this function everytime we get a request to any of our API endpoint.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
