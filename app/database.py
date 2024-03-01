from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
import psycopg2
# it is used to access the column name while retreiving the data from the database
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# it is the database url format
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# encoded_password = urllib.parse.quote_plus(settings.database_password)
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
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


# we are using this while loop because once the connection failed try to connect again before executing the remaining codes.
# this is only used when we want to execute raw sql queries directly using the library psycopg2
# while True:
#     try:
#         # cursor_factory=REalDictCursoe returns rows as dictionaries with column names as keys
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='abhidharsh@1999', cursor_factory=RealDictCursor)
#         # The cursor object allows you to execute SQL queries
#         cursor = conn.cursor()
#         print('Database connected sucessfully')
#         break
#     except Exception as error:
#         print('Database connection failed')
#         print('Error: ', error)
#         # it will wait for 2sec and try to connect again
#         time.sleep(2)
