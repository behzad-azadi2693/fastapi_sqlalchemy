from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional
from fastapi import APIRouter, status, Response, Query, Path, Body, File, UploadFile

class Image(BaseModel):
    url: str
    alias: str

class BlogModelSchema(BaseModel):
    title: str=Body(...,  min_length=8)
    description: str=Body(..., min_length=8)
    phone_number: int=Path(..., ge=1)
    publish: Optional[bool]=False
    tags: list[str]=Body(...,)


