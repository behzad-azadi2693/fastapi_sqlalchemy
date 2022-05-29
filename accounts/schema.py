from pydantic import BaseModel, validator #EmailStr
from fastapi  import Body, Query, Path, UploadFile, File, HTTPException, status


class UserKey(BaseModel):
    id: int
    username:str
    

class UserSchema(BaseModel):
    id: int
    username:str
    email:str
    password: str
    is_active: bool

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username:str = Body(..., min_length=4, max_length=250)
    email:str    = Body(..., max_length=250, regex="([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")


class UserIn(UserBase):
    password:str          = Body(..., min_length=8, max_length=150, regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
    password_confierm:str = Body(..., min_length=8, max_length=150, regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")

    @validator('password_confierm')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=400, detail='password do not match')
        return v


class UserOut(UserBase):
    email: str


class UserLogin(BaseModel):
    username: str = Body(..., min_length=4, max_length=250)
    password: str = Body(..., min_length=8)


class ProfileModelSchema(BaseModel):
    fullname: str = Body(None) 
    title: str = Body(None)
    description:str = Body(None)

    class Config:
        orm_mode = True


class ProfileImageSchema(BaseModel):
    image: list[UploadFile] = File(None)

    @validator('image')
    def imgae_valid(cls, v, **kwargs):
        if not v.content_type in ['image/png', 'image/jpg', 'image/jpeg']:
            raise HTTPException(status_code=400, detail='image must be png, jpg, jpeg')
        return v