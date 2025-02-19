from fastapi import UploadFile, Form, HTTPException, APIRouter,Depends
from uuid import uuid4  #用于生成唯一的文件名，以防止文件名冲突。
import os        #用于文件和目录操作。
import re
from schemas import *
from models import *
from settings import UPLOAD_DIR
from typing import List,Optional
from app.login import get_current_user

app_article = APIRouter()
os.makedirs(UPLOAD_DIR, exist_ok=True)





@app_article.post("/article/",tags=['发表文章'])
async def create_article(
                         images:Optional[List[UploadFile]] = None, #图片可以为空
                         tags: Optional[List[str]] = Form([]),#tags可以为空
                         title: str = Form(...), 
                         content: str = Form(...),
                         user: str = Depends(get_current_user)
                         ):
    if images:
        for image in images:
            file_name = f"{uuid4().hex}_{image.filename}"  # 使用 uuid4() 生成唯一文件名
            file_path = os.path.join(UPLOAD_DIR, file_name)  # 存储路径

            # 保存文件
            with open(file_path, "wb") as buffer:
                buffer.write(await image.read())

            # 将图片路径替换到文章内容中
            content = content.replace(f"![{image.filename}]", f"![{image.filename}]({file_path})")
    # 创建文章记录
    article = await Articles.create(title=title, content=content, user_id=user.user_id)
        
    # 处理标签
    if tags:
        tag_objects = []  # 存储传入标签和数据库标签的并集
        for tag_name in tags:
            tag_obj, created = await Tags.get_or_create(tag_name=tag_name)  # 获取或创建标签
            tag_objects.append(tag_obj)
        # 查询数据库中的标签
        choose_tags = await Tags.filter(tag_name__in=[tag.tag_name for tag in tag_objects])
        # 关联标签到文章
        await article.tags.add(*choose_tags)

    return {"message": "Article and images uploaded successfully"}








@app_article.get("/article/{article_id}",tags=['查看文章'])
async def get_article(article_id: int):
    article = await Articles.get(article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
        # 更新阅读次数
    article.view_count += 1
    await article.save() 

    tags_id = await article.tags.all().values("tag_name")  # 查询相关标签

    if tags_id:
        return {
        "article":article, "tags": tags_id
    }
    return {"article":article}
 # 返回文章内容（Markdown 格式，可以转换为 HTML）









@app_article.put("/article/{input_article_id}",tags=['修改文章'])
async def modify_article(
                         input_article_id:int,
                         images:Optional[List[UploadFile]] = None, #图片可以为空
                         tags: Optional[List[str]] = Form([]),#tags可以为空
                         title: str = Form(...), 
                         content: str = Form(...),
                         user: str = Depends(get_current_user),
                         
                         ):
    # 检查文章是否存在，并且用户是否有权限删除该文章
    article = await Articles.filter(article_id=input_article_id).first()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    if article.user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to delete this article",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if images:
        # 先删除旧图片
        old_images = []  # 存储旧图片的文件路径，稍后用来删除
        # 提取当前文章中的图片路径
        for match in re.findall(r'!\[.*?\]\((.*?)\)', article.content):
            old_images.append(match)

        # 删除旧图片
        for old_image_path in old_images:
        # 旧的图片路径存储在文章中，检查路径是否存在，删除文件
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # 上传新图片
        for image in images:
            file_name = f"{uuid4().hex}_{image.filename}"  # 使用 uuid4() 生成唯一文件名
            file_path = os.path.join(UPLOAD_DIR, file_name)  # 存储路径

            # 保存文件
            with open(file_path, "wb") as buffer:
                buffer.write(await image.read())
            # 将图片路径替换到文章内容中
            content = content.replace(f"![{image.filename}]", f"![{image.filename}]({file_path})")
     # 更新文章的标题和内容
    article.title = title
    article.content = content
    await article.save()  # 保存修改


     # 处理标签更新
    if tags:
        # 获取或创建标签
        tag_objects = []
        for tag_name in tags:
            tag_obj, created = await Tags.get_or_create(tag_name=tag_name)
            tag_objects.append(tag_obj)
        # 查询数据库中的标签
        choose_tags = await Tags.filter(tag_name__in=[tag.tag_name for tag in tag_objects])
        # 更新文章的标签
        await article.tags.clear()  # 清除旧的标签
        await article.tags.add(*choose_tags)  # 添加新的标签

    return {"message": "Article and images modify successfully"}








@app_article.delete("/article/",tags=['删除文章'])
async def delete_article(
                         input_article_id: int,
                         user = Depends(get_current_user),
                         ):
    # 检查文章是否存在，并且用户是否有权限删除该文章
    article = await Articles.filter(article_id=input_article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    if article.user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to delete this article",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

       # 删除文章与标签的关联
    await article.tags.clear()  # 清除文章和标签之间的关系

    # 删除文章中的图片
    old_images = []  # 存储旧图片的文件路径，稍后用来删除
    for match in re.findall(r'!\[.*?\]\((.*?)\)', article.content):
        old_images.append(match)

    # 删除图片文件
    for old_image_path in old_images:
        if os.path.exists(old_image_path):
            os.remove(old_image_path)

    # 删除文章本身
    await article.delete()

    return {"message": "Article and associated images deleted successfully"}



