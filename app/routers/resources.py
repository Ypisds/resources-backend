from ..dependencies import get_resource_service
from typing import Annotated
from ..services.resources_service import ResourceService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
async def get_hello_world(service: Annotated[ResourceService, Depends(get_resource_service)]):
    name: str = service.name
    return {"message": "Rota de recursos funcionando", "nameService": name}