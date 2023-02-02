import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import base64
from enum import Enum
from typing import TypedDict, Tuple, NamedTuple, Optional


def _hashing(value: str) -> str:
    salt = '22gyJL22'
    hash_bytes = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=value.encode('utf-8'),
        salt=salt.encode('utf-8'),
        iterations=100000
    )
    return hash_bytes.hex()


def encode_base64(value: str) -> str:
    value_bytes = value.encode('utf-8')
    value_base64 = base64.b64encode(value_bytes).decode()
    return value_base64


def decode_base64(value: str) -> str:
    value_base64_bytes = value.encode('utf-8')
    value_bytes = base64.b64decode(value_base64_bytes).decode('utf-8')
    return value_bytes


class Auth:
    pass


class Password(str):
    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, _hashing(value))


@dataclass(unsafe_hash=True)
class ModelUser:
    first_name: str
    last_name: str
    patronymic: str
    email: str
    login: str
    password: str


class Header(TypedDict):
    alg: str
    typ: str


class Payload(TypedDict):
    sub: str
    iat: str
    exp: str


class InvalidToken(Exception):
    pass


class JWTToken:
    header: Header
    payload: Payload

    @classmethod
    def get_jwt_token_from_token(cls, token: str):
        try:
            header, payload, signature = token.split(".")
        except IndexError:
            raise InvalidToken('Invalid token')

        hashed_signature = _hashing(f"{header}.{payload}")
        if hashed_signature != signature:
            raise InvalidToken('Invalid token')

        decoded_header = decode_base64(header)
        decoded_payload = decode_base64(payload)
        json_header = decoded_header.replace("'", "\"")
        json_payload = decoded_payload.replace("'", "\"")
        return cls(header=json.loads(json_header), payload=json.loads(json_payload))

    def __init__(self, header, payload):
        self.header = header
        self.payload = payload

    def __str__(self):
        header_base64 = encode_base64(str(self.header))
        payload_base64 = encode_base64(str(self.payload))
        signature_hash = _hashing(f"{header_base64}.{payload_base64}")
        return f'{header_base64}.{payload_base64}.{signature_hash}'


LIFE_TIME_ACCESS_TOKEN = 30
LIFE_TIME_REFRESH_TOKEN = 1440


class Tokens(NamedTuple):
    access: str
    refresh: str


class InvalidPassword(Exception):
    pass


class Authorization(Auth):
    def __init__(self, user: ModelUser, password: str):
        self._user = user
        self._password = password
        self._datetime = datetime.now()

    def __call__(self) -> Tokens:
        self._check_password()
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        payload_for_access = {
            "sub": self._user.login,
            "iat": f"{self._datetime}",
            "exp": f"{self._datetime + timedelta(minutes=LIFE_TIME_ACCESS_TOKEN)}",
        }
        payload_for_refresh = {
            "sub": self._user.login,
            "iat": f"{self._datetime}",
            "exp": f"{self._datetime + timedelta(minutes=LIFE_TIME_REFRESH_TOKEN)}",
        }
        return Tokens(
            access=str(JWTToken(header, payload_for_access)),
            refresh=str(JWTToken(header, payload_for_refresh)),
        )

    def _check_password(self) -> None:
        if self._user.password != Password(self._password):
            raise InvalidPassword('Invalid password')


class Authentication(Auth):
    def __init__(self, token: Optional[str]):
        self.token = token

    def check_tokens(self):
        payload = JWTToken.get_jwt_token_from_token(self.token).payload
        exp = datetime.strptime(payload['exp'], '%Y-%m-%d %H:%M:%S.%f')
        if exp < datetime.now():
            return payload['sub']
