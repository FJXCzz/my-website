#这个文件夹存放可多次使用的函数
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
from models import *


async def is_username_exists(username: str) -> bool:
        # 查询是否有相同的用户名
    return await Users.get_or_none(username=username)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):   #比较登录时密码是否和数据库加密后密码相同
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str)-> str:    #加密密码
    return pwd_context.hash(password)