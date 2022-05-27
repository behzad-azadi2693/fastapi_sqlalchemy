import jwt
from sqlalchemy.orm import Session
from config.models import UserModel
from .utils import check_name, psw_ctx, router, get_current_user
from config.settings import get_db, SECRET_KEY
from sqlalchemy.sql import exists
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
            Path, Body, status, Depends, 
            HTTPException, File, UploadFile, Form
        )
from .schema import (
            UserBase, UserIn, UserOut, UserLogin, UserSchema,
            ProfileImageSchema, ProfileModelSchema
        )


@router.post('/create/user/', response_model=UserOut)
async def create_user(user:UserIn=Depends(), db=Depends(get_db)):
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


@router.get('/my/profile/', response_model=UserSchema)
def me(user: UserSchema=Depends(get_current_user)):
    return user


@router.post('/create/profile/{id:int}')
def create_profile(id:int, profile:ProfileModelSchema, 
                images:ProfileImageSchema=Depends(), db=Depends(get_db)):
    user = db.query(exists().where(UserModel.id == id)).scalar()
    if not user:
        raise HTTPException(status_code=400, detail='user is not exists')
    if images is not None:
        for img in images:
            pass