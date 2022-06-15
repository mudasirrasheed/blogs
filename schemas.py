from pydantic import BaseModel
from typing import List
class BlogBase(BaseModel):
     title: str
     body: str
class Blog(BlogBase):
     #id: int
     #creator_id: int
     class Config:
        orm_mode = True

class User(BaseModel):
     name: str
     email: str
     description: str
     password: str
     
class ShowUser(BaseModel):
     #id: int
     name: str
     description: str
     email: str
     
     blogs: List[Blog]=[]
     class Config:
            orm_mode = True
#want only title and body and id

class ShowBlog(BaseModel):
     #id: int
     title: str  #only return title of blog
     body: str
     #Because the required information is present above parent class
     class Config:
            orm_mode = True 