from .schema import (
            UserBase, UserIn, UserOut, UserLogin, 
            ProfileImageSchema, ProfileModelSchema
        )
from sqlalchemy.orm import Session
from config.models import UserModel
from .utils import check_name
from config.db import get_db
from passlib.context import CryptContext
from fastapi import (
            APIRouter, Path, Body, status, Depends, 
            HTTPException, File, UploadFile, Form
        )

router = APIRouter(prefix='/accounts', tags=['Accounts',])

psw_hash = CryptContext(schemes='bcrypt', deprecated='auto')


@router.post('/create/user/', response_model=UserOut)
async def create_user(user:UserIn, db=Depends(get_db)):
    check_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if check_user:
        raise HTTPException(status_code=400, detail='this user is existed')

    add_user = UserModel(
        username = user.username,
        email = user.email,
        password = psw_hash.hash(user.password)
    )
    
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    return user


@router.post('/login/')
async def login(user: UserLogin):
    pass


@router.get('/logout/')
async def logout():
    return 'ok'


@router.post('/create/profile/{id:int}')
def create_profile(id:int, profile:ProfileModelSchema, 
                images:ProfileImageSchema=Depends(), db=Depends(get_db)):
    user = db.query(exists().where(UserModel.id == id)).scalar()
    if not user:
        raise HTTPException(status_code=400, detail='user is not exists')
    if images is not None:
        for img in images:
            pass