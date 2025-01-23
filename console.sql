show databases
show tables
create database website

create table users
(
	user_id int auto_increment primary key comment '用户id',
    username varchar (10) not null unique comment '用户名',
    password varchar (24) not null comment '用户密码',
    gender char (1) default '2' comment '性别1男0女2保密',
    nickname varchar (10) not null comment '用户昵称',
    avatar_path varchar (255) comment '用户头像路径',
    birthday date comment '用户生日',
    registration_time datetime comment '注册时间',
    point int default 0 comment '积分'
);

create table articles (
    article_id int auto_increment primary key comment '文章id',
    creator_id int comment '发表用户id',
    create_time datetime not null comment '发表时间',
    update_time datetime not null comment '更新时间',
    title varchar(50) not null comment '文章标题',
    content longtext not null  comment '文章内容',
    view_count int default 0 comment '浏览量',
    like_count int default 0 comment '点赞数',
    comment_count int default 0 comment '评论数',
    constraint fk_articles_users foreign key (creator_id) references users(user_id)  on delete set null
);
-- crester_id关联users表中的user_id,在删除用户时creater_id设为null

create table tags(
    tag_id int auto_increment primary key comment '标签id',
    tag_name varchar(20) not null unique comment '标签名称'
);

create table articles_tag_association(
    article_id int not null comment '文章id外键',
    tag_id int not null comment '标签id外键',
    constraint fk_article_id foreign key (article_id) references articles(article_id)  on delete cascade ,
    constraint fk_tag_id foreign key (tag_id) references tags(tag_id)  on delete cascade
);
--这张表张表存储文章和标签多对多的关系，表中只有两个外键，在文章或标签删除时也删除对应关系

create table  collects(
    collect_id int auto_increment primary key comment '收藏id',
    collect_time date comment '收藏时间',
    collector_id int not null comment '收藏用户id',
    article_id int  comment '收藏文章id',
    constraint fk_collector_user_id foreign key (collector_id) references users(user_id) on delete cascade ,
    constraint fk_article_id foreign key (article_id) references articles(article_id) on delete set null
);
--这张表存储用户收藏文章的关系，当用户注销时删除对应关系，当收藏文章被删除时置为null

create table comments(
    comment_id int auto_increment primary key comment'评论id',
    creator_id int comment '发表评论用户id',
    parent_comment_id int comment '父评论id 0为直接评论文章',
    article_id int not null comment '评论文章id',
    create_time datetime not null comment '评论时间',
    content text not null comment '评论内容',
    like_count int default 0 comment '点赞数',
    constraint fk_creator_user_id foreign key (creator_id) references users(user_id) on delete set null ,
    constraint fk_parent_comment_id foreign key (parent_comment_id) references comments(comment_id) on delete set null ,
    constraint fk_article_id foreign key (article_id) references articles(article_id) on delete cascade
);
--这张表存储文章评论的关系，当评论用户注销时设为null，父评论删除时置为null，所评论文章删除时同样删除评论

create table messages(
    message_id int auto_increment primary key  comment '消息id',
    senter_id int comment '发送者id',
    receiver_id int comment '接收者id',
    sent_time int comment '发送时间',
    content text not null comment '消息内容',
    message_status char(1) default 1 '消息状态1代表未读0已读',
    constraint fk_senter_id foreign key (senter_id) references users(user_id) on delete cascade ,
    constraint fk_receiver_id foreign key (receiver_id) references users(user_id) on delete cascade
);
--这个表储存私信，发送用户注销时消息删除。

create table subscribes(
    user_id int not null comment '用户id',
    subscribe_id int comment '关注用户的id',
    constraint  fk_sub_user_id foreign key (user_id) references users(user_id) on delete cascade ,
    constraint fk_subscribe_id foreign key (subscribe_id) references users(user_id) on delete set null
);
--关注关系表 用户注销时删除所有关注关系 所关注用户注销时设为空