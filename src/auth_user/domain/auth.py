from typing import NamedTuple, Union
from datetime import datetime, timedelta

from src.auth_user.common.exceptions import InvalidPassword, InvalidToken
from .token import JWTToken
from .model_user import ModelUser
from .utils import hashing


# ToDo: Когда добавим паттерн шина сообщений сделаем create_tokens открытым


class Tokens(NamedTuple):
    access: str
    refresh: str


def _create_tokens(sub: str, iat: datetime) -> Tokens:
    access_token = JWTToken(sub, iat, exp=30)
    refresh_token = JWTToken(sub, iat, exp=14400)
    return Tokens(str(access_token), str(refresh_token))


def authorization(user: ModelUser, password: str) -> Tokens:
    if user.password != hashing(password):
        raise InvalidPassword("Invalid password")
    return _create_tokens(sub=user.login, iat=datetime.now())


def authentication(security_data: str, create_tokens: bool = False) -> Union[Tokens, str]:
    token = JWTToken.get_token_from_security_data(security_data)
    if token.iat + timedelta(minutes=token.exp) < datetime.now():
        raise InvalidToken
    return _create_tokens(sub=token.sub, iat=datetime.now()) if create_tokens else token.sub
