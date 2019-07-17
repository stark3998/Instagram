# -*- coding: utf-8 -*-
from instagram_scraper import db
from instagram_scraper.model.base import Base


class User(Base):
    __tablename__='users'
    username=db.Column(db.String(50))
    handle=db.Column(db.String(25), unique=True)
    posts=db.relationship("Post")

class Post(Base):
    __tablename__='post'
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    img_name=db.Column(db.String(100), unique=True)
    caption=db.Column(db.String(250))
    comments=db.relationship("Comment")

class Comment(Base):
    __tablename__='comment'
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'))
    user=db.Column(db.String(50))
    text=db.Column(db.String(100))