from accounts.schema import UserKey
from pydantic import BaseModel
from .schema import BlogModelSchema
from config.settings import BASE_DIR, get_db
from config.models import BlogModel
from sqlalchemy.orm import Session
from .utils import Status, check_name
from sqlalchemy.sql import exists
from accounts.utils import oauth2_schema, get_current_user
from fastapi import (
            APIRouter, status, Response, Query, Path, Body,
            UploadFile, File, Depends, HTTPException
        )
        
router = APIRouter(prefix='/blog', tags=['Blog',])


@router.get('/list/')
async def blog_list(db=Depends(get_db), summary='get all blogs'):
    blogs_list = db.query(BlogModel).filter(BlogModel.publish.is_(True)).all()
    return blogs_list


@router.get('/{id}/', summary='get blog')
async def blog(id:int, db=Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id, BlogModel.publish.is_(True)).first()
    if blog is not None:
        return blog
    return HTTPException(status_code=404, detail=f'blog with id {id} dos not existe')


@router.post('/create/')
async def create_blog(blog: BlogModelSchema=Depends(), user: UserKey=Depends(get_current_user), db=Depends(get_db)):
    
    file_name = check_name(blog.image.filename, db)
    path_save = f'{BASE_DIR}/media/blog/{file_name}'

    with open(path_save, 'wb') as f:
        image = await blog.image.read()
        f.write(image)

    blog_object = BlogModel(
        title = blog.title,
        description = blog.description ,
        phone_number = blog.phone_number ,
        publish = blog.publish ,
        tags = blog.tags ,
        status = blog.status.name ,
        image = blog.image.filename ,
        user_id = user.id
    )

    db.add(blog_object)
    db.commit()
    db.refresh(blog_object)
    
    return blog_object

@router.delete('/delete/{id:int}')
async def delete_blog(id:int, user: UserKey=Depends(get_current_user), db=Depends(get_db)):
    #blog_exists = db.query(exists().where(BlogModel.id == id)).scalar()
    blog_exists = db.query(BlogModel).filter(BlogModel.id == id).first()
    if blog_exists:
        if blog_exists.user_id.id == user.id:
            db.query(BlogModel).filter(BlogModel.id == id).delete()
            db.commit()

            return {'messages: ', f'blog with id {id} is deleted'}
    
    return HTTPException(status_code=404, detail='Blog Is Not Found')


@router.get('/{user:str}/list/', response_model_include=['id', 'title'])
async def blogs_user(user:str=Path(...,),db=Depends(get_db),response:Response=200, summary='get all blogs'):
    blogs_user = db.query(BlogModel).filter(BlogModel.user.username == user, BlogModel.publish.is_(True)).all()
    
    return blogs_user


