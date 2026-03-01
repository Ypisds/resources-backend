from sqlmodel import SQLModel, Field, Relationship
from typing import List

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True, index=True)
    password: str

    recursos: List["Resource"] = Relationship(back_populates="usuario")


class UserRequest(SQLModel):
    name: str
    username: str
    password: str