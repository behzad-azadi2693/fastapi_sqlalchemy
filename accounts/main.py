from .schema         import UserBase, UserIn, UserOut, UserLogin
from sqlalchemy.orm  import Session
from config.models         import UserModel
from config.db       import get_db
from passlib.context import CryptContext
from fastapi         import (
            APIRouter, Path, Body, status, Depends, 
            HTTPException, File, UploadFile, Form
        )

router = APIRouter(prefix='/accounts', tags=['Accounts',])

psw_hash = CryptContext(schemes='bcrypt', deprecated='auto')


@router.get('/')
async def test(file:str=Form(None)):
    return file


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