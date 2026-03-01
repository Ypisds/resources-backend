from .routers import resources
from contextlib import asynccontextmanager
from .infra.config import settings
from .infra.database import create_db_and_tables, test_connection
from .infra import security

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENV == "dev":
        test_connection()
        create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(resources.router,
                   prefix="/resources",
                    tags=["recursos"]
                )

app.include_router(security.router)





@app.get("/")
async def get_hello_world():
    return {"message": "API fast está funcionando"}