from typing import Dict, List
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):

    class Config():
        orm_mode = True



class UserResponse(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config():
        orm_mode = True



class BlogResponse(BaseModel):
    title: str
    body: str
    creator: UserResponse

    class Config():
        orm_mode = True