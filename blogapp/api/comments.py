from typing import List

from fastapi import APIRouter, Depends, Response, status

# from .blogs import router
from blogapp import schemes
from blogapp.services.comments import CommentsService
from blogapp.services.auth import get_current_user


router = APIRouter(
    prefix="/blogs",
    tags=["comments"]
)

@router.get("/{blog_id}/comments/", response_model=List[schemes.CommentInDB])
def get_comments(
    blog_id: int,
    service: CommentsService = Depends(),
):
    return service.get_all_comments(blog_id)


@router.post('/{blog_id}/', response_model=schemes.CommentInDB)
async def add_comment(
    blog_id: int,
    content: schemes.CommentCreate,
    token_data: str = Depends(get_current_user),
    service: CommentsService = Depends(),
):
    return service.add(content, blog_id, token_data)


@router.put("/{blog_id}/{comment_id}", response_model=schemes.CommentInDB)
async def update_comment(
    blog_id: int,
    comment_id: int,
    content: schemes.CommentUpdate,
    token_data: str = Depends(get_current_user),
    service: CommentsService = Depends()
):
    return service.update(blog_id, comment_id, content, token_data)


@router.delete("/{blog_id}/{comment_id}")
async def delete_comment(
    blog_id: int,
    comment_id: int,
    token_data: str = Depends(get_current_user),
    service: CommentsService = Depends()
):
    service.delete(blog_id, comment_id, token_data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
