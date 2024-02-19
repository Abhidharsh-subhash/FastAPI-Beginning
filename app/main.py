from fastapi import FastAPI
from .import models
from .database import engine
# to resolve the error if the printing is true then the issue is resolved
# import bcrypt
# print(hasattr(bcrypt, '__about__'))
from .routers import post, user, auth, vote
from .config import settings

# this is going to create all of our models in the database as tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "Worlds"}


# this will import all the routes inside the post and user file inside the folder routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
