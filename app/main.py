from .routers import resources

from fastapi import FastAPI

app = FastAPI()

app.include_router(resources.router,
                   prefix="/resources",
                    tags=["recursos"]
                )

@app.get("/")
async def get_hello_world():
    return {"message": "API fast está funcionando"}