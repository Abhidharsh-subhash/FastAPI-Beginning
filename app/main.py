from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
# it is used to define schemas of the data that the user have to send to the server
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
# module to use fastapi with postgres
import psycopg2
# it is used to access the column name while retreiving the data from the database
from psycopg2.extras import RealDictCursor
import time
from .import models, schemas, utils
from .database import engine, get_db
# session is the place where SQLAlchemy keeps track of the data it's working with.
from sqlalchemy.orm import Session
# to resolve the error if the printing is true then the issue is resolved
# import bcrypt
# print(hasattr(bcrypt, '__about__'))
from .routers import post, user, auth


# this is going to create all of our models in the database as tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# we are using this while loop because once the connection failed try to connect again before executing the remaining codes.
while True:
    try:
        # cursor_factory=REalDictCursoe returns rows as dictionaries with column names as keys
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='abhidharsh@1999', cursor_factory=RealDictCursor)
        # The cursor object allows you to execute SQL queries
        cursor = conn.cursor()
        print('Database connected sucessfully')
        break
    except Exception as error:
        print('Database connection failed')
        print('Error: ', error)
        # it will wait for 2sec and try to connect again
        time.sleep(2)


my_posts = [{'id': 1, 'title': 'Statuatory warning', 'content': 'Smoking is injurious to health'},
            {'id': 2, 'title': 'I love to eat', 'content': 'Shawai is my favorite food'}]


@app.get("/")
def read_root():
    return {"Hello": "Worlds"}


# this will import all the routes inside the post and user file inside the folder routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
