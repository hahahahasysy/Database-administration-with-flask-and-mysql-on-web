# models.py

from exts import db
from datetime import datetime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(100), unique=True, nullable=True)  # 用户唯一标识
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=True)
    identity = db.Column(db.String(50), nullable=True)  # 身份
    avatar = db.Column(MEDIUMTEXT, nullable=True)  # 头像（base64）
    jointime = db.Column(db.DateTime, default=datetime.now)
    articles = db.relationship('ArticleModel', back_populates='user')
    likes = db.relationship('LikedArticle', back_populates='user')
    aoharu_posts = db.relationship('AoharuModel', back_populates='user')

class ArticleModel(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    type1 = db.Column(db.String(200), nullable=False)
    type2 = db.Column(db.String(200), nullable=False)
    time1 = db.Column(db.String(200), nullable=False)
    foreigenname1 = db.Column(db.String(200))
    people1 = db.Column(db.String(200))
    content1 = db.Column(db.Text, nullable=False)
    content2 = db.Column(db.Text)
    link = db.Column(db.String(400))
    jointime = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('UserModel', back_populates='articles')
    likes = db.relationship('LikedArticle', back_populates='article')


class LikedArticle(db.Model):
    __tablename__ = "like_article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('UserModel', back_populates='likes')

    auth = db.Column(db.Integer, nullable=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    article = db.relationship('ArticleModel', back_populates='likes')


# 历史事件表
class HistoryModel(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(200))
    location = db.Column(db.String(200))
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)  # JSON格式存储数组
    images = db.Column(MEDIUMTEXT, default=0)
    tags = db.Column(db.Text)  # JSON格式存储数组


# 学院表
class CollageModel(db.Model):
    __tablename__ = "collage"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(MEDIUMTEXT)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50))
    author = db.Column(db.String(200))
    images = db.Column(MEDIUMTEXT)
    content = db.Column(db.Text, nullable=False)  # JSON格式存储数组


# 青春表
class AoharuModel(db.Model):
    __tablename__ = "aoharu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200, collation='utf8mb4_unicode_ci') ,nullable=False)
    description = db.Column(db.Text)
    image = db.Column(MEDIUMTEXT)
    date = db.Column(db.String(50), nullable=False)
    author_name = db.Column(db.String(200))
    author_avatar = db.Column(MEDIUMTEXT)  # base64或URL
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('UserModel', back_populates='aoharu_posts')
    created_time = db.Column(db.DateTime, default=datetime.now)
   