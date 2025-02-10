#这个表存放数据接收返回时用的类

from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException, status



class Token(BaseModel):
    access_token: str
    token_type: str

class Register(BaseModel):
    username:str=Field(max_length=10, pattern=r'^[a-zA-Z0-9_]+$')
    password:str=Field(min_length=9,max_length=24)
