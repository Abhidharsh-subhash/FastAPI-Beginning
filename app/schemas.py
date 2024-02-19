from typing import Optional
from pydantic import BaseModel, ValidationError, EmailStr
from pydantic.types import conint

# schema defenition while creating a post that is the format of the data to be send to the served side.
# the schema/pydantic model defines the structure of a request and response


class UserBase(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        # the orm_mode will tell the Pydanti model to read the data if it is not a dict.
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    # when the value is not given then True will be the default value
    published: bool = True
    # if not data is provided for the field rating then it will be none
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass

# schema definition for the response from the api


class Post(PostBase):
    owner_id: int
    owner: User

    class Config:
        # the orm_mode will tell the Pydanti model to read the data if it is not a dict.
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        # the orm_mode will tell the Pydanti model to read the data if it is not a dict.
        from_attributes = True


class Tokendata(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  # type: ignore
