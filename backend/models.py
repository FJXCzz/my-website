#这个文件存放映射到数据库的类
from tortoise.models import Model
from tortoise import fields
from enum import Enum

class Gender(Enum):
    MAN = '1'
    WOMAN = '0'
    SECRECY = '2'


class Users(Model):
    user_id = fields.IntField(primary_key=True , auto_increment=True)
    username = fields.CharField(null=False, unique=True, max_length=10, description='用户名')
    hashed_password = fields.CharField(null=False, max_length=128, description='加密后的密码')
    # gender = fields.CharField(max_length=1, description='性别', default='2')
    gender = fields.CharEnumField(Gender, description='性别', default=Gender.SECRECY)
    nickname = fields.CharField(default='昵称', null=True,max_length=10, description='用户昵称')
    avatar = fields.BinaryField(description='用户头像')
    birthday = fields.DateField(default='2000-01-01', null=True, description='生日')
    introduction = fields.TextField(default='该用户没写自我介绍', null=True, description='个人介绍')
    registration_time = fields.DatetimeField(auto_now_add=True,description='注册时间')
    # point = fields.IntField(default=0, description='积分')


class Articles(Model):
    article_id = fields.IntField(primary_key=True , auto_increment=True)
    user = fields.ForeignKeyField('models.Users', related_name='articles', on_delete=fields.SET_NULL, null=True, description='发表用户id')
    create_time = fields.DatetimeField(auto_now_add=True,description='发表时间')
    update_time = fields.DatetimeField(auto_now=True,description='更新时间')
    title = fields.CharField(null=False, max_length=50, description='文章标题')
    content = fields.TextField(null=False, description='Markdown 格式的文章内容')
    view_count = fields.IntField(default=0, description='浏览量')
    # like_count = fields.IntField(default=0, description='点赞数')
    # comment_count = fields.IntField(default=0, description='评论数')
    tags = fields.ManyToManyField('models.Tags', related_name='articles_tags', on_delete=fields.CASCADE, description='文章和标签外键')


class Tags(Model):
    tag_id = fields.IntField(primary_key=True, auto_increment=True, description='标签id')
    tag_name = fields.CharField(max_length=20, unique=True, description='标签名称')

    
class Collects(Model):
    collect_id = fields.IntField(primary_key=True, auto_increment=True, description='收藏id')
    collect_time = fields.DateField(auto_now_add=True,description='收藏时间')
    user = fields.ForeignKeyField('models.Users', related_name='collects', on_delete=fields.CASCADE, description='收藏用户id')
    article = fields.ForeignKeyField('models.Articles', related_name='collects', on_delete=fields.CASCADE, description='收藏文章id')


class Comments(Model):
    comment_id = fields.IntField(primary_key=True, auto_increment=True, description='评论id')
    user = fields.ForeignKeyField('models.Users', related_name='comments', on_delete=fields.CASCADE, description='发表评论用户id')
    # parent_comment = fields.ForeignKeyField('models.Comments', default=None, related_name='replies', on_delete=fields.SET_NULL, null=True, description='父评论id 0为直接评论文章')
    article = fields.ForeignKeyField('models.Articles', related_name='comments', on_delete=fields.CASCADE, description='评论文章id')
    create_time = fields.DatetimeField(auto_now_add=True, description='评论时间')
    content = fields.TextField(description='评论内容')

