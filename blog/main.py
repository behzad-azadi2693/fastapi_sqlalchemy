from fastapi import APIRouter, status, Response, Query, Path, Body
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(prefix='/blog', tags=['blog'])


@router.get('/all/', status_code = status.HTTP_200_OK, tags=['v1'])
def blog_all(user_name:str=None, phone_number:int=None, response:Response=200, summary='get all blogs'):
    if user_name and phone_number:
        return {'messages':'blog all'}

    response.status_code = status.HTTP_404_NOT_FOUND
    return "False"


@router.get('/{id}/', tags=['v1'], summary='get blog')
def blog(id:int):
    return {'messages':f'blog {id}'}

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str=Body(...,  min_length=8, max_length=12)
    description: str=Body(..., min_length=8, max_length=12)
    phone_number: int=Path(..., ge=1)
    publish: Optional[bool]=False
    tags: list[str]=Body(...,)
    meta_data: Dict[str, str] = {"key":"value"}
    image: Image = None
    
@router.post('/create/')
def create_post(blog: BlogModel):
    return {'blog': blog}


@router.post('/create/new/{id}/')
def new_post(
            blog:BlogModel, 
            id:int=Path(..., ge=1),
            comment_id:int=Query(None, title='new blog', description='this new blog', deprecated='CommentId'),
            passsword: str=Body(..., min_length=8, max_length=12, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
            ):
    return {'id':{id}, 'blog':blog, 'comment_id':comment_id, 'password':password}