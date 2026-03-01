from ..dependencies import get_resource_service
from typing import Annotated
from ..services.resources_service import ResourceService
from app.models.resource import ResourceCreateRequest
from fastapi import APIRouter, Depends, status
from ..infra.security import get_current_user
from ..models.user import User

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recurso(
    service: Annotated[ResourceService, Depends(get_resource_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    request_body: ResourceCreateRequest,
):
    return service.cadastrar_recurso(request_body, current_user)


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def atualizar_recurso(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ResourceService, Depends(get_resource_service)],
    recurso: ResourceCreateRequest,
):
    return service.atualizar_recurso(recurso, id, current_user)
