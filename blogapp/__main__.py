import uvicorn

from blogapp.settings import settings

uvicorn.run(
    "blogapp.app:app",
    host=settings.server_host,
    port=settings.server_port,
    reload=True 
)