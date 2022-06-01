from typing import Any, List

from fastapi import HTTPException, status


from blogapp import schemes, models
from blogapp.services.base import BaseService


class CommentsService(BaseService):
    # def __get_author(self, username: str) -> models.User:
    #     author = (
    #         self.session
    #         .query(models.User)
    #         .filter_by(username=username)
    #         .first()
    #     )
    #     if not author:
    #         raise HTTPException(status_code=404)
    #     return author
    
    # def __get_blog(self, blog_id: int) -> models.Blog:
    #     blog = (
    #         self.session
    #         .query(models.Blog)
    #         .filter_by(id=blog_id)
    #         .first()
    #     )
    #     if not blog:
    #         raise HTTPException(status_code=404)
    #     return blog
    
    # def __get_comment(self, comment_id) -> models.Comment:
    #     comment = (
    #         self.session
    #         .query(models.Comment)
    #         .filter_by(id=comment_id)
    #         .first()
    #     )
    #     if not comment:
    #         raise HTTPException(status_code=404)
    #     return comment
    
    # def __check_author_credential(self, comment_data: models.Comment, token_data: schemes.TokenData):
    #     permission_exception = HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Only author have permission to change this comment"
    #     )
    #     token_owner_data = self.__get_author(token_data.username)
    #     if not comment_data.is_by == token_owner_data.id:
    #         raise permission_exception

    def get_all_comments(self, blog_id: int) -> List[models.Comment]:
        blog: models.Blog = self._get_model_by(
            models.Blog,
            params={"id": blog_id}
        )
        
        comments = (
            self.session
            .query(models.Comment)
            .filter_by(is_on=blog.id)
            .all()
        )
        return comments

    def add(
        self, 
        comment_data: schemes.CommentCreate,
        blog_id: int, 
        token_data: schemes.TokenData
    ) -> models.Comment:
        author: models.User = self._get_model_by(
            models.User,
            {"username": token_data.username}
        )

        comment = models.Comment(
            is_on=blog_id,
            is_by=author.id,
            content=comment_data.content
        )
        self.session.add(comment)
        self.session.commit()

        return comment
    
    def update(
        self,
        blog_id: int,
        comment_id: int,
        comment_data: schemes.CommentUpdate,
        token_data: schemes.TokenData,
    ) -> models.Comment:
        blog: models.Blog = self._get_model_by(
            models.Blog,
            params={"id": blog_id}
        )

        comment: models.Comment = self._get_model_by(
            models.Comment,
            params={"id": comment_id}
        )
        if not comment.is_on == blog.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The comment not found"
            )

        self._verify_credential(comment.is_by, token_data)

        for field, value in comment_data:
            setattr(comment, field, value)
        self.session.commit()
        return comment

    def delete(
        self,
        blog_id: int,
        comment_id: int,
        token_data: schemes.TokenData
    ) -> None:
        blog: models.Blog = self._get_model_by(
            models.Blog,
            params={"id": blog_id}
        )

        comment: models.Comment = self._get_model_by(
            models.Comment,
            params={"id": comment_id}
        )
        if not comment.is_on == blog.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The comment not found"
            )

        self._verify_credential(comment.is_by, token_data)

        self.session.delete(comment)
        self.session.commit()
        

    
    
        

