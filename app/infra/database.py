from sqlmodel import SQLModel, create_engine, Session, text
from .config import settings
from app.models.user import User
from app.models.resource import Resource

url = settings.DATABASE_URL
connect_args = {"check_same_thread": False} if "sqlite" in url else {}
echo = True if settings.ENV == "dev" else False

engine = create_engine(url, connect_args=connect_args, echo=echo)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def test_connection():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
            print("Conexão bem sucedida")
    except Exception as e:
        print("Conexão falhou")
