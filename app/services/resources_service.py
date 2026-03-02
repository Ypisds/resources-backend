from dataclasses import dataclass
from typing import Annotated
from sqlmodel import Session, select, func, desc
from app.infra.database import get_session
from fastapi import Depends, HTTPException, status
from app.models.resource import (
    Resource,
    ResourceCreateRequest,
    ResourceResponse,
    TipoResource,
)
from app.models.user import User
from app.models.page import Page
from pydantic import PositiveInt


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

        return None

    def listagem_recursos(
        self,
        titulo: str | None,
        tipo: TipoResource | None,
        tags: list[str] | None,
        page: PositiveInt = 1,
        size: PositiveInt = 10,
    ) -> Page[ResourceResponse]:
        statement = select(Resource)

        if titulo:
            statement = statement.where(Resource.titulo.ilike(f"%{titulo}%"))

        if tipo:
            statement = statement.where(Resource.tipo == tipo)

        if tags:
            for tag in tags:
                statement = statement.where(Resource.tags.contains(tag))

        total_query = select(func.count()).select_from(statement.subquery())
        total = self.db.exec(total_query).one()

        items_query = (
            statement.order_by(desc(Resource.id)).offset((page - 1) * size).limit(size)
        )
        items = self.db.exec(items_query).all()

        items_response = [ResourceResponse.model_validate(item) for item in items]

        return Page[ResourceResponse](
            items=items_response,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
        )
