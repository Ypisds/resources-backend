from ..dependencies import get_resource_service
from typing import Annotated
from ..services.resources_service import ResourceService
from fastapi import APIRouter, Depends
from ..infra.security import get_current_user
from ..models.user import User

router = APIRouter()


@router.get("/")
async def get_hello_world(service: Annotated[ResourceService, Depends(get_resource_service)],
                          current_user: Annotated[User, Depends(get_current_user)]
                          ):
    name: str = service.name
    return {"message": "Rota de recursos funcionando", "nameService": name}