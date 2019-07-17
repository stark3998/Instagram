# -*- coding: utf-8 -*-
__author__ = ''

from instagram_scraper.model.insta import User, Post, Comment
from instagram_scraper import ma
from instagram_scraper.schemas import safe_execute

class UserSchema(ma.ModelSchema):
    posts=ma.Nested('PostSchema',many=True)
    class Meta:
        model=User
        exclude=('created_at','updated_at')

class PostSchema(ma.ModelSchema):
    comments=ma.Nested('CommentSchema',many=True)
    class Meta:
        model=Post
        exclude=('created_at','updated_at')

class CommentSchema(ma.ModelSchema):
    class Meta:
        model=Comment
        exclude=('created_at','updated_at')