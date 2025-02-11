#这个表存放数据接收返回时用的类

from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException, status
from datetime import date


class Token(BaseModel):#登录时返回的token
    access_token: str
    token_type: str



class Register(BaseModel):#注册时接收用户名和密码
    username:str=Field(max_length=10, pattern=r'^[a-zA-Z0-9_]+$')
    password:str=Field(min_length=9,max_length=24)


class User_information(BaseModel):
    gender:str=Field(default="2", max_length=1)
    nickname:str=Field(None,max_length=10, pattern=r'^[a-zA-Z0-9_]+$')
    birthday:date | None = Field(None)
    introduction:str | None = Field(None)

