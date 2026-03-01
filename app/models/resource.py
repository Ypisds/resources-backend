from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class TipoResource(str, Enum):
    video = "Vídeo"
    pdf = "PDF"
    link = "Link"


class ResourceCreateRequest(SQLModel):
    titulo: str
    descricao: str | None = Field(default=None, nullable=True)
    tipo: TipoResource
    url: str
    tags: list[str] = Field(default=[], sa_column=Column(JSON))


class Resource(ResourceCreateRequest, table=True):
    id: int | None = Field(default=None, primary_key=True)

    id_usuario: int = Field(foreign_key="users.id")
    usuario: "User" = Relationship(back_populates="recursos")


class ResourceResponse(ResourceCreateRequest):
    id: int
