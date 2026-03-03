from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.models.resource import TipoResource
from typing import Annotated
from app.dependencies import get_ia_service
from app.services.ia_service import IaResponse, IaService
from app.models.user import User
from app.infra.security import get_current_user


class IaRequest(BaseModel):
    titulo: str
    tipo: TipoResource


router = APIRouter()


@router.post("/")
async def receber_sugestao_ia(
    service: Annotated[IaService, Depends(get_ia_service)],
    request_body: IaRequest,
    current_user: Annotated[User, Depends(get_current_user)],
) -> IaResponse:
    request_dict = request_body.model_dump()
    return service.sugerir_descricao_e_tags(**request_dict)
