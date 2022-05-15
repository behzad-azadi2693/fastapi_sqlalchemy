from pydantic import BaseModel, validator
from fastapi import Body, Query, Path


class UserModelSchema(BaseModel):
    username: str=Body(..., min_length=4, max_length=250)
    email: str=Body(..., min_length=4, max_length=250)
    password: str=Body(..., min_length=8, max_length=150, regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
    password_confierm: str=Body(..., min_length=8, max_length=150, regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")

    @validator('password_confierm')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('password do not match')
        return v
        

class OutPutUserSchame(BaseModel):
    username: str
    email: str


class LoginUserSchema(BaseModel):
    username: str=Body(..., min_length=4, max_length=250)
    password: str=Body(..., min_length=8)
 