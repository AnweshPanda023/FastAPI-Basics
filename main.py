from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.app_name)
from app.api.auth import router as auth_router


@app.get("/")
def home():
    return {
        "app": settings.app_name,
        "debug": settings.debug,
    }

app.include_router(auth_router)