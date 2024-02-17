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
# it creates session objects,autocommit=False means You'll need to manually commit changes using the session's commit() method after each transaction
# bind=engine means  specifies the database engine to which the session will be bound
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# declarative_base() means a function provided by SQLAlchemy that creates a base class for declarative class definitions which is used to define database models.
Base = declarative_base()
# we ge a session to our database and everytime we got a request we get a session and after the request is done then close it out.
# we can keep calling this function everytime we get a request to any of our API endpoint.

# Dependency function to create a database session


def get_db():
    db = SessionLocal()  # Create a database session using SessionLocal
    try:
        yield db  # Yield the session to the endpoint function
    finally:
        db.close()  # Close the session after the request is processed
