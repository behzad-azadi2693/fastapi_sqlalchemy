import os
from accounts.schema import UserKey
from pydantic import BaseModel
from .schema import BlogModelSchema, blogList, CommentModelSchema
from config.settings import BASE_DIR, get_db
from config.models import BlogModel, UserModel, CommentBlogModel
from sqlalchemy.orm import Session
from .utils import Status, check_name
from sqlalchemy.sql import exists
from accounts.utils import oauth2_schema, get_current_user
from typing import List, Optional
from fastapi import (
            APIRouter, status, Response, Query, Path, Body,
            UploadFile, File, Depends, HTTPException, BackgroundTasks
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
    
    file_name = check_name(blog.image.filename, db, user.get('id'))
    path_save = f"{BASE_DIR}/media/{user.get('username')}/blog/{file_name}"

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
        user_id = user.get('id')
    )

    db.add(blog_object)
    db.commit()
    db.refresh(blog_object)
    
    return blog_object

@router.delete('/delete/{id:int}')
async def delete_blog(id:int, user: UserKey=Depends(get_current_user), db=Depends(get_db)):
    #blog_exists = db.query(exists().where(BlogModel.id == id)).scalar()
    blog_exists = db.query(BlogModel).filter(BlogModel.id == id, BlogModel.user_id == user.get('id')).first()
    if blog_exists:
            blog = db.query(BlogModel).get(id)
            db.delete(blog)
            db.commit()
            os.remove(os.path.join(BASE_DIR, 'media' , user.get('username'), 'blog', blog_exists.image))
            return {'messages: ', f'blog with id {id} is deleted'}
    
    return HTTPException(status_code=404, detail='Blog Is Not Found')


@router.get('/my/blog/list/', response_model_include=['id', 'title'])
async def blogs_user(db=Depends(get_db),user: UserKey=Depends(get_current_user), summary='get all blogs'):
    blogs_user = db.query(BlogModel).filter(BlogModel.user_id == user.get('id')).all()
    
    return blogs_user


@router.get('/for/{username:str}/', response_model_exclude={'id'})
async def blog_for(username:str=Path(...,), db=Depends(get_db)):
    user = db.query(exists().where(UserModel.username == username)).scalar()
    if user:
        blog = db.query(BlogModel).filter(BlogModel.user.has(username = username)).all()
        return blog
    
    return HTTPException(status_code=400, detail='user is not exist')


@router.post('/comment/create/{id:int}/')
async def comment_create(comment:CommentModelSchema, db=Depends(get_db),id:int=Path(...)):
    blog = db.query(BlogModel).get(id)

    if not blog:
        return HTTPException(status_code=404, detail='blog is not found')

    new_comment = CommentBlogModel(
        name = comment.name,
        email = comment.email,
        messages = comment.messages,
        blog_id = blog.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return comment


@router.get('/all/comment/')
async def all_comment(db=Depends(get_db)):
    all = db.query(CommentBlogModel).all()
    return all