from typing import Generic, TypeVar, List
from pydantic import Field, BaseModel, PositiveInt

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int = Field(default=0, ge=0)
    page: PositiveInt = Field(default=1)
    size: PositiveInt = Field(default=10)
    pages: int = Field(default=0, ge=0)
