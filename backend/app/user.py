# /user_id   主页 展示收藏和个人发表文章时间降序 个人信息 get
# user_id/collect  /user_id的收藏 get
# user_id/article  /user_id的文章 get

from fastapi import APIRouter,Depends,UploadFile, Response
from app.login import get_current_user
from models import *
from schemas import *

app_user = APIRouter()

#查看更改个人信息接口

@app_user.get('/user/{userid}',response_model=User_infor_out,tags=['获取个人信息'])
async def get_user_Information(userid:int):
    user = await Users.get(user_id = userid)
    return user

#修改更改个人信息接口
@app_user.put('/user/setting',tags=['修改个人信息'])
async def update_user_Information(userin: User_infor_update, 
                                  user: str = Depends(get_current_user)):

    data = userin.model_dump()
    await Users.filter(username=user.username).update(**data)
    return Response(status_code=200,content='修改成功')


@app_user.put('/user/avatar',tags=['修改头像'])
async def update_avatar(avatar: UploadFile,
                        user: str = Depends(get_current_user)):

    avatar_content = await avatar.read()
    await Users.filter(username=user.username).update(avatar=avatar_content)
    return Response(status_code=200,content='修改成功')
    


