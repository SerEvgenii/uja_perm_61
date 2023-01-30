from dataclasses import dataclass
from datetime import datetime
import hashlib
import base64


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


@dataclass(frozen=True)
class JWTToken:
    header: str
    payload: str
    signature: str

    def __str__(self):
        header_base64 = encode_base64(self.header)
        payload_base64 = encode_base64(self.payload)
        signature = header_base64 + payload_base64
        signature_hash = _hashing(signature)
        return encode_base64(f'{header_base64}.{payload_base64}.{signature_hash}')


class Authorization(Auth):
    def __init__(self, user: ModelUser, password: str):
        self._user = user
        self._password = password
        self.datetime = datetime.now()

    def get_jwt_token(self) -> JWTToken:
        header = str({
            'alg': 'HS256',
            'typ': 'JWT'
        })
        payload = str({
            'sub': self._user.login,
            'iat': self.datetime.strftime("%m/%d/%Y, %H:%M:%S")
        })
        signature = ""
        return JWTToken(header, payload, signature)
