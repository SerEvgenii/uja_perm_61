from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class ModelUser:
    first_name: str
    last_name: str
    patronymic: str
    email: str
    login: str
    password: str
