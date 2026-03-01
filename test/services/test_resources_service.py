from fastapi.testclient import TestClient
from app.services.resources_service import ResourceService
from app.models.resource import ResourceCreateRequest, TipoResource
from app.main import app
from app.models.user import User
from unittest.mock import MagicMock, ANY
from sqlmodel import Session

client = TestClient(app)


def test_create_resource():
    db_mock = MagicMock(spec=Session)

    user = User(id=1, name="nome", username="login", password="password")
    request = ResourceCreateRequest(
        titulo="titulo",
        descricao="descrição",
        tipo=TipoResource.pdf,
        url="www.teste.com",
        tags=["bom", "mal"],
    )

    service = ResourceService(db=db_mock)

    service.cadastrar_recurso(request, user)

    db_mock.add.assert_called_once_with(ANY)
    db_mock.commit.assert_called_once()
