from fastapi import (
        APIRouter, status, Response, Query, Path, Body,
        UploadFile, File, Depends
    )
from pydantic import BaseModel
from .schema import BlogModelSchema
from config.db import BASE_DIR, get_db
from .models import BlogModel
from sqlalchemy.orm import Session
from .utils import Status, check_name

router = APIRouter(prefix='/blog', tags=['Blog',])

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
async def create_post(status:Status, blog: BlogModelSchema=Depends(), file: UploadFile=File(...), db=Depends(get_db)):
    file_name = check_name(file.filename, db)
    path_save = f'{BASE_DIR}/media/blog/{file_name}'

    with open(path_save, 'wb') as f:
        image = await file.read()
        f.write(image)

    blog_object = BlogModel(
        **blog.dict(), status=status, image = file_name
    )
    db.add(blog_object)
    db.commit()
    db.refresh(blog_object)
    
    return blog_object


@router.post('/create/new/{id}/')
async def new_post(
            blog:BlogModelSchema, 
            id:int=Path(..., ge=1),
            comment_id:int=Query(None, title='new blog', description='this new blog', deprecated='CommentId'),
            description: str=Body(..., min_length=8, max_length=250)
            ):
    return {'id':{id}, 'blog':blog, 'comment_id':comment_id, 'password':password}