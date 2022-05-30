from pydantic import BaseModel
from typing import Union


class UserListRespone(BaseModel):
    id:int
    username:str

    class Config:
        orm_mode = True

class ProfileResponse(BaseModel):
    fullname : str  
    title : str
    description : str

    class Config:
        orm_mode = True

class ImageResponse(BaseModel):
    id:int
    image:str

    class Config:
        orm_mode = True

class UserRespone(BaseModel):
    username:str
    email:str
    is_active:bool
    image:list[ImageResponse]
    profile:list[ProfileResponse]

    class Config:
        orm_mode = True

class BlogResponse(BaseModel):
    id:int
    title:str
    image:str

    class Config:
        orm_mode = True

class UserProfileResponse(BaseModel):
    username:str
    email:str
    image:list[ImageResponse]
    profile:list[ProfileResponse]
    blogs:list[BlogResponse]

    class Config:
        orm_mode = True