from django.db import IntegrityError

from src.auth_user.common.exceptions import UserAlreadyExists, InvalidSecurityData
from src.auth_user.adapters.repository import AbstractRepository
from src.auth_user.domain.model_user import ModelUser
from src.auth_user.domain.auth import authorization
from src.auth_user.domain.utils import hashing, decode_base64
from .serializers import UserDetailSerializer


def registration(
        repository: AbstractRepository,
        first_name: str,
        last_name: str,
        patronymic: str,
        email: str,
        login: str,
        password: str) -> dict:
    user = ModelUser(first_name, last_name, patronymic, email, login, hashing(password))
    try:
        repository.add(user)
    except IntegrityError:
        raise UserAlreadyExists("User already exists")

    serializer = UserDetailSerializer(user)
    return serializer.data


def authorization_(repository: AbstractRepository, security_data: str) -> dict:
    security_data = decode_base64(security_data)
    try:
        login, password = security_data.split(":")
    except (ValueError, IndexError):
        raise InvalidSecurityData("Invalid security data")

    user = repository.get(login)
    if user is None:
        raise InvalidSecurityData("Invalid security data")

    tokens = authorization(user, password)
    return {"access_token": tokens.access, "refresh_token": tokens.refresh}


def change_password(repository: AbstractRepository, login: str, password: str) -> None:
    user = repository.get(login)
    if user is None:
        raise InvalidSecurityData("Invalid security data")
    user.password = hashing(password)
    repository.update(user)
