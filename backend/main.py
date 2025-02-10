import uvicorn
from fastapi import FastAPI,APIRouter
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from app.register import signup


app = FastAPI()

register_tortoise(

    app = app,
    config = TORTOISE_ORM,
    generate_schemas=True  #在建立连接时，根据模型类生成数据表

)





app.include_router(signup,tags=["用户注册，用户名长度小于10用户名只包含字母（大写或小写）、数字和下划线 _，密码最小长度为9最大24"],)













if __name__ == '__main__':
    uvicorn.run("main:app",host='127.0.0.1',port=8080,reload=True)