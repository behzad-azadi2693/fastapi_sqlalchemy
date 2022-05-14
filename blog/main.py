from fastapi import APIRouter, status, Response, Query, Path, Body
from pydantic import BaseModel
from .schema import BlogModelSchema

router = APIRouter(prefix='/blog', tags=['Blog',])

@router.get('/')
async def index(response_descriptions='this first page'):
    """
    project for **learning**
    """
    return "hello world"


@router.get('/all/', status_code = status.HTTP_200_OK)
async def blog_all(user_name:str=None, phone_number:int=None, response:Response=200, summary='get all blogs'):
    if user_name and phone_number:
        return {'messages':'blog all'}

    response.status_code = status.HTTP_404_NOT_FOUND
    return "False"


@router.get('/{id}/', summary='get blog')
async def blog(id:int):
    return {'messages':f'blog {id}'}


@router.post('/create/')
async def create_post(blog: BlogModelSchema):
    return {'blog': blog}


@router.post('/create/new/{id}/')
async def new_post(
            blog:BlogModelSchema, 
            id:int=Path(..., ge=1),
            comment_id:int=Query(None, title='new blog', description='this new blog', deprecated='CommentId'),
            description: str=Body(..., min_length=8, max_length=250)
            ):
    return {'id':{id}, 'blog':blog, 'comment_id':comment_id, 'password':password}