from fastapi import APIRouter,Depends
from app.login import get_current_user

apptest=APIRouter()
@apptest.get('/test')
async def test(username=Depends(get_current_user)):
    return{'测试成功'}
