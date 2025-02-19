#这个表存放数据接收返回时用的类

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from datetime import date
from models import *

class Token(BaseModel):#登录时返回的token
    access_token: str
    token_type: str



class Register(BaseModel):#注册时接收用户名和密码
    username:str=Field(max_length=10, pattern=r'^[a-zA-Z0-9_]+$')
    password:str=Field(min_length=9,max_length=24)




#修改个人信息时用
class User_infor_update(BaseModel):
    gender:Gender
    nickname:str=Field(max_length=10)
    birthday:date
    introduction:str=Field(max_length=200)


class User_infor_out(User_infor_update):
    avatar:bytes



