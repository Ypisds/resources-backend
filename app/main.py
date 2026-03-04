from .routers import resources, ia
from contextlib import asynccontextmanager
from .infra.config import settings
from .infra.database import create_db_and_tables, test_connection
from .infra import security
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENV == "dev":
        test_connection()

    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(security.router, tags=["auth"])

app.include_router(resources.router, prefix="/resources", tags=["recursos"])

app.include_router(ia.router, prefix="/ai", tags=["ai"])

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://resources-frontend.onrender.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
