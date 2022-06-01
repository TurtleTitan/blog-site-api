from pydantic import BaseModel, Field


class BaseComment(BaseModel):
    content: str


class CommentCreate(BaseComment):
    pass


class CommentUpdate(BaseComment):
    pass


class CommentInDB(BaseComment):
    id: int
    is_on: int = Field(..., gt=0)
    is_by: int = Field(..., gt=0)

    class Config:
        orm_mode = True