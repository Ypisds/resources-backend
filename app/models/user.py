from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True, index=True)
    password: str

class UserRequest(SQLModel):
    name: str
    username: str
    password: str