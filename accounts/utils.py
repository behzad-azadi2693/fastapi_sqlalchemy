import jwt
from config.models import ImageModel, UserModel
from config.settings import get_db, SECRET_KEY
from uuid import uuid4
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import  APIRouter, Depends, HTTPException
from .schema import UserSchema

router = APIRouter(prefix='/accounts', tags=['Accounts',])

psw_ctx = CryptContext(schemes='bcrypt', deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/accounts/login/')


def check_name(name, db, id):
    file_name = db.query(ImageModel).filter(ImageModel.image == name, ImageModel.profile.has(user_id=id)).first()

    if file_name:
        pre, post = name.split('.')
        new_name  = f"{pre}-{uuid4()}.{post}"
        return check_name(new_name, db, id)
    return name


def get_current_user(token: UserSchema=Depends(oauth2_schema), db=Depends(get_db)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user_current = db.query(UserModel).get(payload.get('id'))
    if not user_current:
        return HTTPException(status_code=401, detail='user is not found')
    return {
        'id':user_current.id, 
        'username':user_current.username, 
        'email':user_current.email, 
        'password':user_current.password,
        'is_active':user_current.is_active
        }
 