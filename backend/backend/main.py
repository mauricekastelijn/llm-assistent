from fastapi import FastAPI
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from api.routes import api_router
from core.context import Context
from utils.logger import logger

from uuid import uuid4
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    load_dotenv()
    load_dotenv("secrets/.env")

    unique_id = uuid4().hex[0:8]
    os.environ["LANGCHAIN_PROJECT"] = f"LLM app - {unique_id}"

    logger.info("Initializing context...")
    _ = Context()

    yield

    logger.info("Application shutting down...")


app = FastAPI(title="Personal Assistant Backend", lifespan=lifespan)

# Include API routes
app.include_router(api_router)
