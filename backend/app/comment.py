from fastapi import HTTPException, APIRouter,Depends
from schemas import *
from models import *
from app.login import get_current_user



app_comment = APIRouter()


@app_comment.post("/comment",tags=["发表评论"])

async def add_comment(article_id:int,
                      content:str,
                      user = Depends(get_current_user)):
     #查看文章是否存在
     article = await Articles.get_or_none(article_id=article_id)
     if not article:
          raise HTTPException(status_code=404, detail="Article not found")
     
     # 检查评论内容长度（可选）
     if len(content) > 500:  # 假设最大长度为 500 字符
          raise HTTPException(status_code=400, detail="Content is too long")
     #添加评论
     await Comments.create(article_id=article_id,user_id=user.user_id,content=content)
     return{"message": "Comment successfully"}


@app_comment.delete("/comment/{comment_id}",tags=["删除评论"])

async def delete_comment(comment_id: int, 
                         user = Depends(get_current_user)):
    # 查看评论是否存在
    comment = await Comments.get_or_none(comment_id=comment_id, user_id=user.user_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # 删除评论
    await comment.delete()
    
    return {"message": "Comment deleted successfully"}




@app_comment.get("/article/comment",tags=["根据文章查评论"])

async def get_aeticle_comment(article_id:int, page: int = 1):
    # 每页显示 10 条评论
    page_size = 10
    # 计算分页的起始位置
    offset = (page - 1) * page_size
    # 获取指定文章的评论
    comments = await Comments.filter(article_id=article_id).order_by(Comments.created_time.desc()).offset(offset).limit(page_size).all()
     # 获取评论的总数
    comments_count = await Comments.filter(article_id=article_id).count()
    # 计算总页数
    total_pages = (comments_count + page_size - 1) // page_size  # 向上取整
    return{
        "comments": comments,
        "total_count": comments_count,
        "total_pages": total_pages,
        "current_page": page
    }




@app_comment.get("/user/comment",tags=["根据用户查评论"])

async def get_aeticle_comment(page: int = 1,
                              user = Depends(get_current_user)):
    
     
    # 每页显示 10 条评论
    page_size = 10
    # 计算分页的起始位置
    offset = (page - 1) * page_size

    # 获取当前用户的评论，按时间倒序排序
    comments = await Comments.filter(user_id=user.user_id).order_by(Comments.created_time.desc()).offset(offset).limit(page_size).all()

    # 获取评论的总数
    comments_count = await Comments.filter(user_id=user.user_id).count()
     # 计算总页数
    total_pages = (comments_count + page_size - 1) // page_size  # 向上取整
    return{
        "comments": comments,
        "total_count": comments_count,
        "total_pages": total_pages,
        "current_page": page
    }

