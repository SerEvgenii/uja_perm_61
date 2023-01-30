from typing import Optional, List

from django.test import TestCase

from src.auth_user.adapters.repository import AbstractRepository
from src.auth_user.domain.authorization import ModelUser, encode_base64, Password
from src.auth_user.service_layer.service import registration, authorization


class FakeRepository(AbstractRepository):
    def __init__(self, users: List[ModelUser]):
        self._users = set(users)

    def get(self, login: str) -> Optional[ModelUser]:
        try:
            return next(user for user in self._users if user.login == login)
        except StopIteration:
            return None

    def add(self, model_user: ModelUser) -> None:
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
    # @classmethod
    # def setUpClass(cls):
    #     model_user = ModelUser(
    #         first_name='firstname1',
    #         last_name='lastname1',
    #         patronymic='patronymic1',
    #         email='email1',
    #         login='login1',
    #         password='password1'
    #     )
    #     cls.model_user = model_user
    #     repository = DjangoORMRepository()
    #     repository.add(model_user)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     User.objects.filter(login='login1').delete()

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
                'login': 'login2',
            }
        )

    def test_authorization(self):
        model_user = ModelUser(
            first_name='firstname1',
            last_name='lastname1',
            patronymic='patronymic1',
            email='email1',
            login='login1',
            password=Password('password1')
        )
        security_data = encode_base64('login1:password1')
        token = authorization(FakeRepository([model_user]), security_data)
        self.assertIsInstance(token, str)

    # def test_user_exists_exception(self):
    #     data = [
    #         'firstname1',
    #         'lastname1',
    #         'patronymic1',
    #         'email1',
    #         'login1',
    #         'password1',
    #     ]
    #     self.assertRaises(UserExists, registration, *data)
    #
    # def test_invalid_security_data_exception(self):
    #     login = 'login1'
    #     password = 'password1'
    #     data = login + password
    #     data_base64 = encode_base64(data)
    #     self.assertRaises(InvalidSecurityData, authorization, data_base64)
    #
    # def test_user_not_found_exception(self):
    #     login = 'login2'
    #     password = 'password1'
    #     data = login + ':' + password
    #     data_base64 = encode_base64(data)
    #     self.assertRaises(InvalidSecurityData, authorization, data_base64)
    #
    # def test_invalid_password_exception(self):
    #     login = 'login1'
    #     password = 'password2'
    #     data = login + ':' + password
    #     data_base64 = encode_base64(data)
    #     self.assertRaises(InvalidPassword, authorization, data_base64)
