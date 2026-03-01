from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock
from app.services.resources_service import ResourceService
from app.models.user import User
from app.dependencies import get_resource_service
from app.infra.security import get_current_user
from fastapi import status

client = TestClient(app)


user = User(id= 1, name="nome", username="login", password="password")

def test_create_resource():
    app.dependency_overrides[get_current_user] = lambda: user

    service = MagicMock(spec=ResourceService)

    app.dependency_overrides[get_resource_service] = lambda: service

    payload={
        "titulo": "titulo",
        "descricao": "descricao",
        "tipo": "PDF",
        "url": "www.teste.com",
        "tags": ["bom", "ruim"]
    }

    response = client.post('/resources', json=payload)

    service.cadastrar_recurso.assert_called_once()
    assert response.status_code == status.HTTP_201_CREATED

def test_create_resource_with_error():
    app.dependency_overrides[get_current_user] = lambda: user

    service = MagicMock(spec=ResourceService)

    service.cadastrar_recurso.side_effect = Exception("Deu um erro")

    app.dependency_overrides[get_resource_service] = lambda: service

    payload={
        "titulo": "titulo",
        "descricao": "descricao",
        "tipo": "PDF",
        "url": "www.teste.com",
        "tags": ["bom", "ruim"]
    }

    response = client.post('/resources', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST