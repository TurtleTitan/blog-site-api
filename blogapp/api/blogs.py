from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status

from blogapp import schemes
from blogapp.services.auth import get_current_user
from blogapp.services.blogs import BlogsService


router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


@router.get('/', response_model=List[schemes.Blog])
async def get(
    filter: Optional[str] = None,
    service: BlogsService = Depends()
):
    return service.get_all(filter)


@router.get('/{blog_id}/', response_model=schemes.Blog)
async def get(
    blog_id: int,
    service: BlogsService = Depends()
):
    return service.get(blog_id)    


@router.post('/', response_model=schemes.Blog)
async def post(
    blog_data: schemes.BlogCreate,
    token_data: str = Depends(get_current_user),
    service: BlogsService = Depends()
):
    return service.create(blog_data, token_data)


@router.put('/{blog_id}/', response_model=schemes.Blog)
async def update(
    blog_id: int,
    blog_data: schemes.BlogUpdate,
    token_data: str = Depends(get_current_user),
    service: BlogsService = Depends()
):
    return service.update(blog_id, blog_data, token_data)


@router.delete('/{blog_id}/')
async def delete(
    blog_id: int,
    token_data: str = Depends(get_current_user),
    service: BlogsService = Depends()
):
    service.delete(blog_id, token_data)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
