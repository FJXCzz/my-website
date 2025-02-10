from fastapi import APIRouter, HTTPException, status,Response
from schemas import Register
from models import *
from func import *
from passlib.context import CryptContext
from func import is_username_exists

signup = APIRouter()

@signup.post('/register')

async def register(user:Register):

    a = await is_username_exists(user.username)
    if a:
        raise HTTPException(status_code=409,detail='用户名已存在')


    #加密密码
    hashed_password = get_password_hash(user.username)
    #保存用户名和加密后的密码
    try:
        result = await Users.create(username=user.username,hashed_password=hashed_password)
        print(result.username)
        return Response(status_code=201,content='用户创建成功')
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

