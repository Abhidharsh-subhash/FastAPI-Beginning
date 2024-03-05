from fastapi import FastAPI
from .import models
from .database import engine
# to resolve the error if the printing is true then the issue is resolved
# import bcrypt
# print(hasattr(bcrypt, '__about__'))
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

# this is going to create all of our models in the database as tables
# removing it as now alembic will handle all the interations with the database
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# these are the list of domain from where the APIs can be accessed
origins = ['*']
app.add_middleware(
    # middleware is a function that runs before every request
    CORSMiddleware,
    # what domains should be able to talk to our APIs
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/sample")
def read_root():
    return {"message": "bind mount works"}


@app.get("/")
async def custom_swagger_ui_html():
    return get_swagger_ui_html(title="My API Documentation", openapi_url="/openapi.json")

# this will import all the routes inside the post and user file inside the folder routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
