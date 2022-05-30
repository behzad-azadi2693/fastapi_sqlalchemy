from pydantic import BaseModel
from datetime import datetime

class BlogListResponse(BaseModel):

    id : int    
    title : str  
    image : str
    created : datetime  
    
    class Config:
        orm_mode = True


class CommentResponse(BaseModel):
    name:str
    email:str
    messages:str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id:int
    username:str
    
    class Config:
        orm_mode = True

class BlogSingleResponse(BaseModel):
    id:int
    title:str        
    description:str   
    phone_number:int
    tags:str
    status:str        
    image:str         
    created:datetime      
    comments:list[CommentResponse]
    
    class Config:
        orm_mode = True


class BlogCreateResponse(BaseModel):
    id:int
    title:str        
    description:str   
    phone_number:int
    tags:str
    status:str        
    image:str         
    created:datetime      
    
    class Config:
        orm_mode = True