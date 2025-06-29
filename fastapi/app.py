import os
import asyncpg
from fastapi import FastAPI
from dotenv import load_dotenv
from routes import routes
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", "172.27.176.1")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

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
