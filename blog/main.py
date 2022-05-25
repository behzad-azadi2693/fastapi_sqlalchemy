from pydantic       import BaseModel
from .schema        import BlogModelSchema
from config.db      import BASE_DIR, get_db
from config.models        import BlogModel
from sqlalchemy.orm import Session
from .utils         import Status, check_name
from fastapi        import (
            APIRouter, status, Response, Query, Path, Body,
            UploadFile, File, Depends
        )
        
router = APIRouter(prefix='/blog', tags=['Blog',])


@router.get('/all/', status_code = status.HTTP_200_OK)
async def blog_all(db=Depends(get_db),response:Response=200, summary='get all blogs'):
    blogs_list = db.query(BlogModel).filter(BlogModel.publish.is_(True))
    return blogs_list


@router.get('/{id}/', summary='get blog')
async def blog(id:int):

    return {'messages':f'blog {id}'}


@router.post('/create/')
async def create_post(blog: BlogModelSchema=Depends(), db=Depends(get_db)):
    
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