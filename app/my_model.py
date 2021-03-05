
from fastapi import FastAPI
from pydantic import BaseModel , Field , EmailStr





class postschema(BaseModel):
    title: str = Field(...)
    body : str = Field(...)
    likes : int = Field(default=None)
    comment : list = Field(default=None)
    id : int = Field(default=None)


class postschema_response(BaseModel):
    title: str = Field(...)
    body : str = Field(...)
    #likes : int = Field(default=None)
    #comment : list = Field(default=None)
    

class comment_post(BaseModel):
    body : str = Field(...)
    id : int = Field(...)

    

class my_user(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    usertype: str = Field(...)

class userLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    usertype: str = Field(...)


