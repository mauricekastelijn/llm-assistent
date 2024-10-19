import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from api.routes import api_router
from core.context import Context
from utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    load_dotenv(os.getenv("BACKEND_SECRETS_FILE", ".env"))
    logger.info("Initializing context...")
    _ = Context()

    yield
    logger.info("Application shutting down...")


app = FastAPI(title="Personal Assistant Backend", lifespan=lifespan)

# Include API routes
app.include_router(api_router)
