from ..dependencies import get_resource_service
from typing import Annotated
from ..services.resources_service import ResourceService
from app.models.resource import ResourceCreateRequest, TipoResource
from fastapi import APIRouter, Depends, status, Query
from ..infra.security import get_current_user
from ..models.user import User
from pydantic import BaseModel, PositiveInt

router = APIRouter()


class ListagemQuery(BaseModel):
    titulo: str | None = None
    tipo: TipoResource | None = None
    tags: list[str] | None = None
    page: PositiveInt = 1
    size: PositiveInt = 10


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


@router.get("/", status_code=status.HTTP_200_OK)
async def listagem(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ResourceService, Depends(get_resource_service)],
    query_params: Annotated[ListagemQuery, Query()],
):
    return service.listagem_recursos(**query_params.model_dump())


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_recurso(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ResourceService, Depends(get_resource_service)],
):
    return service.excluir_recurso(id, current_user)
