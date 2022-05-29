import jwt, os, shutil
from sqlalchemy.orm import Session
from config.models import UserModel, ImageModel, ProfileModel
from .utils import check_name, psw_ctx, router, get_current_user, user_dependency
from config.settings import get_db, SECRET_KEY, BASE_DIR
from sqlalchemy.sql import exists
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
            Path, Body, status, Depends, Response, Request,
            HTTPException, File, UploadFile, Form, BackgroundTasks
        )
from .schema import (
            UserBase, UserIn, UserOut, UserLogin, UserSchema,
            ProfileImageSchema, ProfileModelSchema, UserKey
        )


@router.get('/all/user/')
async def all_user(db=Depends(get_db)):
    list_user = db.query(UserModel).all()
    return list_user


@router.post('/create/user/', response_model=UserOut)
async def create_user( background_tasks:BackgroundTasks,user:UserIn=Depends(), db=Depends(get_db)):
    check_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if check_user:
        raise HTTPException(status_code=400, detail='this user is existed')

    add_user = UserModel(
        username = user.username,
        email = user.email,
        password = psw_ctx.hash(user.password)
    )

    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    background_tasks.add_task(user_dependency, add_user, db)

    return user


@router.post('/login/')
async def login(data:OAuth2PasswordRequestForm=Depends(), db=Depends(get_db)):
    username = data.username
    password = data.password

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail='user not found')
    elif not psw_ctx.verify(password , user.password):
        raise HTTPException(status_code=400, detail='password not correct')

    user_dict = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
    }
    access_token = jwt.encode(user_dict, SECRET_KEY)


    return {'access_token': access_token, 'token_type': 'bearer'}


@router.delete('/remove/user/')
async def remove_user(db=Depends(get_db), user:UserKey=Depends(get_current_user)):
    user_is = db.query(UserModel).filter(UserModel.id == user.get('id')).one()
    db.delete(user_is)
    db.commit()
    shutil.rmtree(os.path.join(BASE_DIR, 'media', user.get('username')))
    return HTTPException(status_code=200, detail='user is delete')


@router.delete('/remove/image/{id:int}/')
async def remove_image(user:UserKey=Depends(get_current_user), db=Depends(get_db), id:int=Path(..., ge=1)):

    picture = db.query(ImageModel).get(id)
    
    if picture:
        db.query(ImageModel).filter(ImageModel.user_id == user.get('id'), ImageModel.id == id).delete()
        db.commit()
        os.remove(os.path.join(BASE_DIR, 'media', user.get('username'), 'profile', picture.image))
        return HTTPException(status_code=400, detail='image is delete')
    else:
        return HTTPException(status_code=404, detail='image not found')

    return 'ok'

@router.get('/image/all/{username:str}')
async def all_image(username:str=Path(...,), db=Depends(get_db)):
    images = db.query(ImageModel).filter(ImageModel.user.has(username=username)).all()
    
    return images


@router.post('/add/image/profile/')
async def add_image_profile(user: UserKey=Depends(get_current_user),image:UploadFile=File(...,), db=Depends(get_db)):

    file_name = check_name(image.filename, db, user.get('id'))
    path_save = f"{BASE_DIR}/media/{user.get('username')}/profile/{file_name}"

    with open(path_save, 'wb') as f:
        image = await image.read()
        f.write(image)

    new_image = ImageModel(
        image = file_name ,
        user_id = user.get('id')
    )

    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    
    return new_image


@router.get('/user/information/')
async def my_information(user:UserKey=Depends(get_current_user), db=Depends(get_db)):
    my_user = db.query(UserModel).get(user.get('id'))
    return my_user


@router.get('/user/profile/')
async def create_profile(user:UserKey=Depends(get_current_user), db=Depends(get_db)):
    profile = db.query(ProfileModel).get(user.get('id'))
    return profile


@router.put('/update/profile/')
async def create_profile(profile:ProfileModelSchema,user:UserKey=Depends(get_current_user), db=Depends(get_db)):
    
    obj = db.query(ProfileModel).get(user.get('id'))
    obj.full_name = profile.fullname,
    obj.title = profile.title,
    obj.description = profile.description
    db.commit()

    return new_profile


@router.get('/profile/user/{username:str}/')
async def profile_user(username:str=Path(...,), db=Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.user.has(username=username)).one()

    return profile