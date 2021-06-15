from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    

class User(UserBase):
    password: str




class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):

    class Config():
        orm_mode = True



class UserResponse(UserBase):
    blogs: List[Blog]

    class Config():
        orm_mode = True



class BlogResponse(BlogBase):
    creator: UserResponse = {}

    class Config():
        orm_mode = True