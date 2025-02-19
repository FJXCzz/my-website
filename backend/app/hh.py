from fastapi import APIRouter,Depends,UploadFile,Form,File
from app.login import get_current_user
from typing import Optional,List

apptest=APIRouter()
@apptest.get('/test')
async def test(user=Depends(get_current_user)):
    user
    return{'测试成功':user}

@apptest.post("/file")

async def get_file(file: Optional[UploadFile] = File(None)):
    if file:
        return {"filename": file.filename}
    return {"message": "No file uploaded"}