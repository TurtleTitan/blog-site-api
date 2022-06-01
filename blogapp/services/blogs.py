from datetime import datetime
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from blogapp import models, schemes
from blogapp.database import get_session
from blogapp.services.base import BaseService


class BlogsService(BaseService):
    def get_all(self, filter: Optional[str] = None) -> List[models.Blog]:
        query = self.session.query(models.Blog)
        if filter:
            query = query.filter(models.Blog.title.contains(filter.lower()))
        blogs = query.all()
        return blogs
        
    def get(self, blog_id: int) -> models.Blog:
        return self._get_model_by(
            models.Blog,
            params={"id": blog_id}
        )

    def create(self, blog_data: schemes.BlogCreate, token_data: schemes.TokenData) -> models.Blog:
        data = blog_data.dict()
        author: models.User = self._get_model_by(
            models.User,
            {"username": token_data.username}
        )

        data.update({
            'author_id': author.id,
            'publication_date': datetime.now()
        })

        blog = models.Blog(**data)
        self.session.add(blog)
        self.session.commit()
        return blog

    def update(self, blog_id: int, blog_data: schemes.BlogUpdate, token_data: schemes.TokenData) -> models.Blog:
        blog: models.Blog = self._get_model_by(
            models.Blog,
            params={"id": blog_id}
        )
        self._verify_credential(blog.author_id, token_data)
    
        for field, value in blog_data:
            setattr(blog, field, value)
        self.session.commit()
        return blog

    def delete(self, blog_id: int, token_data: schemes.TokenData):
        blog: models.Blog = self._get_model_by(
            models.Blog,
            params={"id": blog_id}
        )
        self._verify_credential(blog.author_id, token_data)

        self.session.delete(blog)
        self.session.commit()
        
        
    
