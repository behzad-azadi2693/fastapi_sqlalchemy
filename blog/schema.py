from pydantic import BaseModel, HttpUrl, validator
from typing import List, Dict, Optional
from .utils import Status
from enum import Enum
from fastapi import ( 
            APIRouter, status, Response, Query, Path, 
            Body, File, UploadFile, HTTPException
        )


class BlogModelSchema(BaseModel):
    title: str = Body(...,  min_length=8)
    description: str = Body(..., min_length=8)
    phone_number: int = Path(..., ge=1)
    publish: Optional[bool] = False
    tags: list[str] = Body(...,)
    status: Status
    image: UploadFile = File(...,)

    class Config:
        orm_mode = True

    @validator('image')
    def check_image(cls, v, **kwargs):
        if not v.content_type in ['image/png', 'image/jpg', 'image/jpeg']:
            return HTTPException(status_code=400, detail='filds must be image')
        return v

class CommentModelSchema(BaseModel):
    name: str = Body(..., mon_lengt=3)
    email:str    = Body(..., max_length=250, regex="([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    messages: str = Body(..., min_length=8)

    class Config:
        orm_mode = True
