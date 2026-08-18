from fastapi import FastAPI

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.exceptions.handlers import (
    register_exception_handlers,
)
from app.api.admin import router as admin_router

app = FastAPI(title=settings.app_name)


@app.get("/")
def home():
    return {
        "app": settings.app_name,
        "debug": settings.debug,
    }


register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
