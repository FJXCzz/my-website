from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import Token
import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from schemas import *
from models import *


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
#OAuth2PasswordBearer 用于获取从客户端发送来的 OAuth2 的 "Bearer token"
# （也就是 JWT token 或者其他类型的访问令牌）。tokenUrl="api/login" 参数指定了
# 获取 token 的 API 路径，这里是 /api/login


applogin = APIRouter()



def verify_password(plain_password, hashed_password):   #比较登录时密码是否和数据库加密后密码相同
    return pwd_context.verify(plain_password, hashed_password)

#比较用户名密码是否正确
async def authenticate_user(username: str, password: str):
    user = await Users.get_or_none(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


#生成token expires_delta是过期时间  
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)#加密密钥。加密算法
    return encoded_jwt



#检查是否登录的函数
async def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # 解码 token
        username: str = token_data.get("sub")# 提取用户名 (sub 字段)
        if username is None:
            raise credentials_exception# 如果没有 sub 字段，抛出认证失败异常
    except InvalidTokenError:
        raise credentials_exception# 捕获 token 解码错误（无效的 token）
    user = await Users.get_or_none(username=username)    # 查找用户
    if user is None:
        raise credentials_exception   # 如果找不到用户，抛出认证失败异常
    return user





#登录接口返回一个token
@applogin.post('/login')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


