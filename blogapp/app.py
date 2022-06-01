from fastapi import FastAPI

from blogapp.api.blogs import router as blogs_router
from blogapp.api.auth import router as test_router
from blogapp.api.comments import router as comments_router

app = FastAPI()
app.include_router(blogs_router)
app.include_router(test_router)
app.include_router(comments_router)
