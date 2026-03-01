from dataclasses import dataclass
from typing import Annotated
from sqlmodel import Session
from app.infra.database import get_session
from fastapi import Depends, HTTPException, status
from app.models.resource import Resource, ResourceCreateRequest, ResourceResponse
from app.models.user import User


@dataclass
class ResourceService:
    db: Annotated[Session, Depends(get_session)]

    def cadastrar_recurso(self, resource: ResourceCreateRequest, user: User):
        resource_dic = resource.model_dump()

        resource_to_save = Resource(**resource_dic, usuario=user)

        self.db.add(resource_to_save)
        self.db.commit()
        self.db.refresh(resource_to_save)

        return ResourceResponse.model_validate(resource_to_save)

    def get_resource_by_id(self, id: int, user: User):
        resource_returned = self.db.get(Resource, id)

        if not resource_returned:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Recurso não existe"
            )

        if resource_returned.id_usuario != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não é o dono do recurso",
            )

        return resource_returned

    def atualizar_recurso(
        self, resource: ResourceCreateRequest, id: int, user: User
    ) -> ResourceResponse:
        resource_returned = self.get_resource_by_id(id=id, user=user)

        updated_data = resource.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(resource_returned, key, value)

        self.db.add(resource_returned)
        self.db.commit()
        self.db.refresh(resource_returned)

        return ResourceResponse.model_validate(resource_returned)

    def excluir_recurso(self, id: int, user: User):
        resource_returned = self.get_resource_by_id(id=id, user=user)

        self.db.delete(resource_returned)
        self.db.commit()
