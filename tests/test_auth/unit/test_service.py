from datetime import datetime
from typing import Optional, List

from django.db import IntegrityError
from django.test import TestCase

from src.auth_user.adapters.repository import AbstractRepository
from src.auth_user.common.exceptions import UserAlreadyExists, InvalidSecurityData
from src.auth_user.domain.model_user import ModelUser
from src.auth_user.domain.token import JWTToken
from src.auth_user.domain.utils import hashing, encode_base64
from src.auth_user.service_layer.service import registration, authorization_, change_password


class FakeRepository(AbstractRepository):
    def __init__(self, users: List[ModelUser]):
        self._users = set(users)

    def get(self, login: str) -> Optional[ModelUser]:
        try:
            return next(user for user in self._users if user.login == login)
        except StopIteration:
            return None

    def add(self, model_user: ModelUser):
        for user in self._users:
            if user.login == model_user.login or user.email == model_user.email:
                raise IntegrityError
        self._users.add(model_user)

    def update(self, model_user: ModelUser) -> None:
        try:
            user = next(user for user in self._users if user.login == model_user.login)
            user.first_name = model_user.first_name
            user.last_name = model_user.last_name
            user.patronymic = model_user.patronymic
            user.email = model_user.email
            user.password = model_user.password
        except StopIteration:
            return


class ServiceTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model_user = ModelUser(
            first_name='firstname1',
            last_name='lastname1',
            patronymic='patronymic1',
            email='email1',
            login='login1',
            password=hashing('password1')
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_registration(self):
        data = registration(
            FakeRepository([]),
            first_name='firstname2',
            last_name='lastname2',
            patronymic='patronymic2',
            email='email2',
            login='login2',
            password='password2'
        )
        self.assertIsInstance(data, dict)
        self.assertDictEqual(
            data,
            {
                'first_name': 'firstname2',
                'last_name': 'lastname2',
                'patronymic': 'patronymic2',
                'email': 'email2',
                'login': 'login2'
            }
        )

    def test_authorization(self):
        security_data = encode_base64('login1:password1')
        token = authorization_(FakeRepository([self.model_user]), security_data)
        self.assertIsInstance(token, dict)

    def test_user_already_exists_exception(self):
        data = [
            'firstname1',
            'lastname1',
            'patronymic1',
            'email1',
            'login1',
            'password1'
        ]
        self.assertRaises(UserAlreadyExists, registration, FakeRepository([self.model_user]), *data)

    def test_invalid_security_data_exception(self):
        security_data = encode_base64('login1password1')
        self.assertRaises(InvalidSecurityData, authorization_, FakeRepository([self.model_user]), security_data)

    def test_user_not_found_exception(self):
        security_data = encode_base64('login2:password1')
        self.assertRaises(InvalidSecurityData, authorization_, FakeRepository([self.model_user]), security_data)

    def test_change_password(self):
        change_password(FakeRepository([self.model_user]), self.model_user.login, "password2")
        self.assertEqual(self.model_user.password, hashing("password2"))
