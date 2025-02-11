# /user_id   主页 展示收藏和个人发表文章时间降序 个人信息 get
# user_id/collect  /user_id的收藏 get
# user_id/article  /user_id的文章 get

from fastapi import APIRouter,Depends,File
from app.login import get_current_user
from models import *
from schemas import *
app_acount_setting = APIRouter()

#查看更改个人信息接口
@app_acount_setting.get('/acount/setting',response_model=User_information,tags=['查看个人信息'])
async def get_account_Information(usename:str=Depends(get_current_user)):
    user = await Users.get(username=usename)
    return user

@app_acount_setting.put('/acount/setting',tags=['修改个人信息'])
async def update_account_Information(userin: User_information, username: str = Depends(get_current_user)):
    data = userin.model_dump()
    Users.filter(username=username).update(**data)
    


#查看更改用户头像接口
@app_acount_setting.get('/acount/avatar',tags=['查看头像'])
async def get_account_avatar(username: str = Depends(get_current_user)):
    user = await Users.get(username=username)
    return user.avatar


@app_acount_setting.put('/acount/avatar',tags=['修改头像'])
async def update_account_avatar(username:str=Depends(get_current_user), avatar:bytes = File()):
    Users.filter(username=username).update(avatar=avatar)
    return 1