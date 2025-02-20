from fastapi import HTTPException, APIRouter,Depends
from schemas import *
from models import *
from app.login import get_current_user


app_collect = APIRouter()



@app_collect.post("/api/article/collect/{article_id}",tags=["添加收藏"])

async def add_collect(article_id:int,
                      user = Depends(get_current_user)):
     #查看文章是否存在
     article = await Articles.get_or_none(article_id=article_id)
     if not article:
          raise HTTPException(status_code=404, detail="Article not found")
     #检查是否已经被收藏
     collect = await Collects.get_or_none(article_id=article_id, user_id=user.user_id)
     if collect:
         raise HTTPException(status_code=409, detail="Article already collect")
     #添加收藏关系
     await Collects.create(article_id=article_id, user_id=user.user_id)
     return{"message": "Collect successfully"}




@app_collect.delete("/api/article/collect/{article_id}",tags=["删除收藏"])

async def delete_collect(article_id:int,
                         user = Depends(get_current_user)):
     #查看文章是否被收藏
     collect = await Collects.get_or_none(article_id=article_id, user_id=user.user_id)
     if not collect:
        raise HTTPException(status_code=404, detail="Collect record not found")
     #删除收藏关系
     await collect.delete()
     return {"message": "Collect deleted successfully"}




@app_collect.get("/api/article/collect",tags=["查看收藏"])

async def get_collect(page: int = 1, user = Depends(get_current_user)):
    # 每页显示 10 条记录
    page_size = 10
    # 计算分页的起始位置
    offset = (page - 1) * page_size

    # 获取当前用户的收藏记录
    collects = await Collects.filter(user_id=user.user_id).order_by(Collects.created_time.desc()).offset(offset).limit(page_size).all()

    # 获取收藏的文章 ID 列表
    article_ids = [collect.article_id for collect in collects]
    
    
    return  {"article_ids": article_ids}
