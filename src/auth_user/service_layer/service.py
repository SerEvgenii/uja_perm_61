from datetime import datetime
from typing import Optional

from django.db import IntegrityError

from src.auth_user.adapters.repository import AbstractRepository
from src.auth_user.domain.authorization import ModelUser, Password, Authorization, decode_base64, JWTToken
from .serializers import UserDetailSerializer


class UserExists(Exception):
    pass


class InvalidSecurityData(Exception):
    pass


class UserNotFound(Exception):
    pass


def registration(repository: AbstractRepository, first_name: str, last_name: str, patronymic: str, email: str, login: str, password: str) -> dict:
    user = ModelUser(first_name, last_name, patronymic, email, login, password)
    try:
        repository.add(user)
    except IntegrityError:
        raise UserExists('User already exists')
    serializer = UserDetailSerializer(user)
    return serializer.data


def authorization(repository: AbstractRepository, security_data: str) -> dict:
    security_data = decode_base64(security_data)
    try:
        login, password = security_data.split(':')
    except IndexError:
        raise InvalidSecurityData('Invalid security data')

    user = repository.get(login)
    if user is None:
        raise InvalidSecurityData('Invalid security data')

    auth = Authorization(user, password)
    tokens = auth()
    return {
        "access_token": tokens.access,
        "refresh_token": tokens.refresh,
    }


def authentication(
        repository: AbstractRepository,
        access_token: Optional[str],
        refresh_token: Optional[str]) -> Optional[ModelUser]:
    if access_token is not None:
        """обращаемся к аутентификации предметной области, передаем ей access token и ждем ответа"""

    elif refresh_token is not None:
        """обращаемся к аутентификации предметной области, передаем ей refresh token и ждем ответа
        если все ок, то обращаемся к авторизации предметной области
        """
    else:
        "как то возмущаемся, т.е. кидаем исключение"





    payload_access_token = JWTToken.create(jwt_token)._payload
    return repository.get(payload_access_token['sub'])
