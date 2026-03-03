from fastapi.testclient import TestClient
from app.services.resources_service import ResourceService
from app.models.resource import ResourceCreateRequest, TipoResource, Resource
from app.main import app
from app.models.user import User
from unittest.mock import MagicMock, ANY
from sqlmodel import Session
from fastapi import status, HTTPException
import pytest

client = TestClient(app)


def test_create_resource():
    db_mock = MagicMock(spec=Session)

    def mock_refresh(obj):
        obj.id = 1

    user = User(id=1, name="nome", username="login", password="password")
    request = ResourceCreateRequest(
        titulo="titulo",
        descricao="descrição",
        tipo=TipoResource.pdf,
        url="www.teste.com",
        tags=["bom", "mal"],
    )

    db_mock.refresh.side_effect = mock_refresh

    service = ResourceService(db=db_mock)

    resposta = service.cadastrar_recurso(request, user)

    db_mock.add.assert_called_once_with(ANY)
    db_mock.commit.assert_called_once()

    assert resposta.id == 1


def test_get_user_by_id():
    db_mock = MagicMock(spec=Session)

    user = User(id=1, name="nome", username="login", password="password")
    resource = Resource(
        id=1,
        titulo="titulo",
        descricao="descricao",
        tipo=TipoResource.link,
        url="www.url.com",
        tags=["oi", "tchau"],
        usuario=user,
        id_usuario=user.id,
    )

    db_mock.get.return_value = resource

    service = ResourceService(db=db_mock)

    resposta = service.get_resource_by_id(1, user)

    assert resposta.id == resource.id


def test_get_user_by_id_error_resource_nao_existe():
    db_mock = MagicMock(spec=Session)
    db_mock.get.return_value = None

    user = User(id=1, name="nome", username="login", password="password")

    service = ResourceService(db=db_mock)

    with pytest.raises(HTTPException) as e:
        service.get_resource_by_id(1, user)

    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert e.value.detail == "Recurso não existe"



def test_atualizar_recurso_com_sucesso():
    db_mock = MagicMock(spec=Session)

    user = User(id=1, name="nome", username="login", password="password")
    request = ResourceCreateRequest(
        titulo="titulo2",
        descricao="descrição2",
        tipo=TipoResource.pdf,
        url="www.teste.com2",
        tags=["bom2", "mal2"],
    )
    resource = Resource(
        id=1,
        titulo="titulo",
        descricao="descricao",
        tipo=TipoResource.link,
        url="www.url.com",
        tags=["oi", "tchau"],
        usuario=user,
        id_usuario=user.id,
    )

    db_mock.get.return_value = resource

    servico = ResourceService(db=db_mock)

    resposta = servico.atualizar_recurso(request, 1, user=user)

    assert resposta.titulo == request.titulo
    assert resposta.descricao == request.descricao
    assert resposta.tipo == request.tipo
    assert resposta.url == request.url
    assert resposta.tags == request.tags

    db_mock.commit.assert_called_once()
    db_mock.add.assert_called_once_with(ANY)
    db_mock.refresh.assert_called_once()


def test_excluir_recurso_com_sucesso():
    db_mock = MagicMock(spec=Session)

    user = User(id=1, name="nome", username="login", password="password")
    resource = Resource(
        id=1,
        titulo="titulo",
        descricao="descricao",
        tipo=TipoResource.link,
        url="www.url.com",
        tags=["oi", "tchau"],
        usuario=user,
        id_usuario=user.id,
    )

    db_mock.get.return_value = resource

    service = ResourceService(db=db_mock)

    service.excluir_recurso(1, user)

    db_mock.delete.assert_called_once_with(ANY)
    db_mock.commit.assert_called_once()
