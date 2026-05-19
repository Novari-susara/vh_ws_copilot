"""
TaskManager API — Sample Python project for VS Code Copilot Demo
A full-featured task management REST API built with FastAPI.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.api.users import router as users_router
from src.utils.database import close_db, init_db
from src.utils.logger import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    setup_logging()
    await init_db()
    logger.info("TaskManager API started successfully")
    yield
    await close_db()
    logger.info("TaskManager API shut down gracefully")


app = FastAPI(
    title="TaskManager API",
    description="A sample task management API for VS Code Copilot demos",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
