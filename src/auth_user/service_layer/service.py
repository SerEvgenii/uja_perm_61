from django.db import IntegrityError

from src.auth_user.adapters.repository import DjangoORMRepository, AbstractRepository
from src.auth_user.domain.authorization import ModelUser, Password, Authorization, decode_base64
from .serializers import UserDetailSerializer


class UserExists(Exception):
    pass


class InvalidSecurityData(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidPassword(Exception):
    pass


def registration(repository: AbstractRepository, first_name: str, last_name: str, patronymic: str, email: str, login: str, password: str) -> dict:
    user = ModelUser(first_name, last_name, patronymic, email, login, password)
    try:
        repository.add(user)
    except IntegrityError:
        raise UserExists('User already exists')
    serializer = UserDetailSerializer(user)
    return serializer.data


def authorization(repository: AbstractRepository, security_data: str) -> str:
    security_data = decode_base64(security_data)
    try:
        login = security_data.split(':')[0]
        password = security_data.split(':')[1]
    except IndexError:
        raise InvalidSecurityData('Invalid security data')

    user = repository.get(login)
    if user is None:
        raise InvalidSecurityData('Invalid security data')
    if user.password != Password(password):
        raise InvalidPassword('Invalid password')

    auth = Authorization(user, password)
    return str(auth.get_jwt_token())
