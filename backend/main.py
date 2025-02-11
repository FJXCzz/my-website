# 先安装require.txt里的东西，有些不全，
# 在settings配置好连接数据库的信息，启动main.py自动在数据库中生成表
# app文件夹存放各项功能的实现

import uvicorn
from fastapi import FastAPI,APIRouter
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM

from app.hh import apptest
from app.register import signup
from app.login import applogin
from app.account import app_acount_setting

app = FastAPI()

register_tortoise(

    app = app,
    config = TORTOISE_ORM,
    generate_schemas=True  #在建立连接时，根据模型类生成数据表

)




app.include_router(apptest, prefix='/api', tags=['测试'])
app.include_router(signup, prefix='/api', tags=["用户注册，用户名长度小于10用户名只包含字母（大写或小写）、数字和下划线 _，密码最小长度为9最大24"],)
app.include_router(applogin, prefix='/api',tags=['登录，返回一个token'])
app.include_router(app_acount_setting, prefix='/api')












if __name__ == '__main__':
    uvicorn.run("main:app",host='127.0.0.1',port=8080,reload=True)