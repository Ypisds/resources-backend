from typing import Annotated
from .services.resources_service import ResourceService
from sqlmodel import Session
from .infra.database import get_session
from fastapi import Depends
from .services.user_service import UserService
from .services.ia_service import IaService


def get_resource_service(
    db: Annotated[Session, Depends(get_session)],
) -> ResourceService:
    return ResourceService(db=db)


def get_user_service(db: Annotated[Session, Depends(get_session)]) -> UserService:
    return UserService(db=db)


def get_ia_service() -> IaService:
    return IaService()
