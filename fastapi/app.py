import os
import asyncpg
from fastapi import FastAPI
from dotenv import load_dotenv
from routes import routes
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for initializing and cleaning up resources.
    """
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    app.state.db_pool = db_pool
    yield
    await db_pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello! Happy to inform you"}

app.include_router(routes.router)

# Allow connection from other services
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
