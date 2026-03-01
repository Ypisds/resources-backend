import pytest
from unittest.mock import MagicMock, ANY
from fastapi.testclient import TestClient
from app.services.user_service import UserService, get_password_hash
from sqlmodel import Session
from app.models.user import User, UserRequest
from fastapi import HTTPException

from app.main import app

client = TestClient(app)


def test_create_user_with_success():
    db_mock = MagicMock(spec=Session)
    db_mock.exec.return_value.first.return_value = None

    service = UserService(db=db_mock)

    request = UserRequest(name="qualquer_nome", username="login", password="senha")

    service.create_user(request)

    db_mock.exec.return_value.first.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.add.assert_called_once_with(ANY)


def test_create_user_with_user_already_exists():
    db_mock = MagicMock(spec=Session)
    db_mock.exec.return_value.first.return_value = User(
        id=1, name="nome", username="login", password="password"
    )

    service = UserService(db=db_mock)

    request = UserRequest(name="qualquer_nome", username="login", password="senha")

    with pytest.raises(HTTPException) as e:
        service.create_user(request)

    assert e.value.status_code == 409
    assert e.value.detail == "Usuário já existe"


def test_get_user_test_with_success():
    db_mock = MagicMock(spec=Session)
    db_mock.exec.return_value.first.return_value = User(
        id=1, name="nome", username="login", password="password"
    )

    service = UserService(db=db_mock)

    user = service.get_user("login")

    assert user.id == 1
    assert user.name == "nome"
    assert user.username == "login"
    assert user.password == "password"


def test_get_user_without_user():
    db_mock = MagicMock(spec=Session)
    db_mock.exec.return_value.first.return_value = None

    service = UserService(db=db_mock)

    user = service.get_user("username")

    assert user is False


def test_authenticate_user_with_success():
    db_mock = MagicMock(spec=Session)
    db_mock.exec.return_value.first.return_value = User(
        id=1, name="nome", username="login", password=get_password_hash("password")
    )

    service = UserService(db=db_mock)

    user = service.authenticate_user("login", "password")

    assert user.id == 1
    assert user.name == "nome"
    assert user.username == "login"


def test_authenticate_user_wrong_password():
    db_mock = MagicMock(spec=Session)
    db_mock.exec.return_value.first.return_value = User(
        id=1, name="nome", username="login", password=get_password_hash("password")
    )

    service = UserService(db=db_mock)

    user = service.authenticate_user("login", "password_wrong")

    assert user is False
