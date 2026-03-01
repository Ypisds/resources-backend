from dataclasses import dataclass
from typing import Annotated
from sqlmodel import Session
from app.infra.database import get_session
from fastapi import Depends
from app.models.resource import Resource, ResourceCreateRequest
from app.models.user import User

@dataclass
class ResourceService:
    db: Annotated[Session, Depends(get_session)]

    def cadastrar_recurso(self,resource: ResourceCreateRequest, user: User):
        resource_to_save = Resource(
            titulo=resource.titulo,
            descricao=resource.descricao,
            tipo=resource.tipo,
            url=resource.url,
            tags=resource.tags,
            usuario=user
        )
        
        self.db.add(resource_to_save)
        self.db.commit()
    

        