from fastapi import APIRouter, HTTPException, Response
from schemas import Register
from models import *


from passlib.context import CryptContext


signup = APIRouter()



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password:str)-> str:    #加密密码
    return pwd_context.hash(password)





@signup.post('/register')
async def register(user:Register):
    #判断用户名是否已存在
    a = await Users.get_or_none(username=user.username)
    if a:
        raise HTTPException(status_code=409,detail='用户名已存在')
    #加密密码
    hashed_password = get_password_hash(user.password)
    #保存用户名和加密后的密码
    try:
        result = await Users.create(username=user.username,
                                    hashed_password=hashed_password,
                                    avatar=b'\x00\x00\x00\x00\x00\x00\x00\x00')
        return Response(status_code=201,content='用户创建成功')
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

