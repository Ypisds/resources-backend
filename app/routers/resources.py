from ..dependencies import get_resource_service
from typing import Annotated
from ..services.resources_service import ResourceService
from app.models.resource import ResourceCreateRequest
from fastapi import APIRouter, Depends, Response, status
from ..infra.security import get_current_user
from ..models.user import User

router = APIRouter()


@router.post("/")
async def create_recurso(
    service: Annotated[ResourceService, Depends(get_resource_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    request_body: ResourceCreateRequest,
):
    try:
        service.cadastrar_recurso(request_body, current_user)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
