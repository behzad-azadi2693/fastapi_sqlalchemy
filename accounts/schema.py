from pydantic import BaseModel
from fastapi import Body, Query, Path


class UserModelSchema(BaseModel):
    username: str=Body(..., min_length=4, max_length=250)
    email: str=Body(..., min_length=4, max_length=250)
    password: str=Body(..., min_length=8, max_length=150, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    password_confierm: str=Body(..., min_length=8, max_length=150, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")


class OutPutUserSchame(BaseModel):
    username: str
    email: str


class LoginUserSchema(BaseModel):
    username: str=Body(..., min_length=4, max_length=250)
    password: str=Body(..., min_length=8)
 