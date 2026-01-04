from pydantic import BaseModel, ConfigDict
from typing import List, Optional
class BlogBase(BaseModel):
    title:str
    body:str

class Blog(BlogBase):
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    name: str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs:List[Blog] = []
    model_config = ConfigDict(from_attributes=True)

class ShowBlog(BaseModel): # To display only the necessary fields
    title:str
    body:str
    owner:ShowUser
    # class Config: # () are optional
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)

class Login(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str] = None
