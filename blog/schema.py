from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi import APIRouter, status, Response, Query, Path, Body

class Image(BaseModel):
    url: str
    alias: str

class BlogModelSchema(BaseModel):
    title: str=Body(...,  min_length=8, max_length=12)
    description: str=Body(..., min_length=8, max_length=12)
    phone_number: int=Path(..., ge=1)
    publish: Optional[bool]=False
    tags: list[str]=Body(...,)
    meta_data: Dict[str, str] = {"key":"value"}
    image: Image = None
    