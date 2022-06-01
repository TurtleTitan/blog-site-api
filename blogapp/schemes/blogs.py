from datetime import datetime

from pydantic import BaseModel


class BaseBlog(BaseModel):
    title: str
    content: str


class Blog(BaseBlog):
    id: int
    author_id: int
    publication_date: datetime

    class Config:
        orm_mode=True


class BlogCreate(BaseBlog):
    pass 


class BlogUpdate(BaseBlog):
    pass