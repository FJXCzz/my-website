from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer




from apps.app01 import app01

from apps.app02 import app02

from apps.app03 import app03

from apps.app04 import app04

from apps.app05 import app05






app = FastAPI()



@app.get("/",tags=["Hello World"])
async def root():
    return {"message": "Hello World"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}




app.include_router(app01,tags=["路径参数，查询参数，请求体"])
app.include_router(app02,tags=["From表单"])
app.include_router(app03,tags=["上传文件"])
app.include_router(app04,tags=["requset对象"])
app.include_router(app05,tags=["响应参数"])






if __name__ == '__main__':
    uvicorn.run("main:app",port=8000,reload=True)

