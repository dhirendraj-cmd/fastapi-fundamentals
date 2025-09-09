from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_tables
from app.account.models import User, RefreshToken



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
