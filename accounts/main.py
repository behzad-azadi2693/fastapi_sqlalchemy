from fastapi import APIRouter, Path, Body, status
from .schema import UserModelSchema, LoginUserSchema, OutPutUserSchame

router = APIRouter(prefix='/accounts', tags=['Accounts',])

@router.post('/create/user/', response_model=OutPutUserSchame)
async def create_user(user:UserModelSchema):
    return user

@router.post('/login/')
async def login(user: LoginUserSchema):
    return 'OK'

@router.get('/logout/')
async def logout():
    return 'ok'