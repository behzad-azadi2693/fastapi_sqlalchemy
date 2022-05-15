from fastapi import APIRouter, Path, Body, status, Depends, HTTPException
from .schema import UserModelSchema, LoginUserSchema, OutPutUserSchame
from sqlalchemy.orm import Session
from .models import UserModel
from config.db import get_db
from passlib.context import CryptContext


router = APIRouter(prefix='/accounts', tags=['Accounts',])

psw_hash = CryptContext(schemes='bcrypt', deprecated='auto')

@router.post('/create/user/')
async def create_user(user:UserModelSchema, db=Depends(get_db)):
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
    return add_user

@router.post('/login/')
async def login(user: LoginUserSchema):
    pass

@router.get('/logout/')
async def logout():
    return 'ok'