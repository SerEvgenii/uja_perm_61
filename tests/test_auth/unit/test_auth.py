from datetime import datetime

from django.test import TestCase

from src.auth_user.common.exceptions import InvalidPassword, InvalidToken
from src.auth_user.domain.model_user import ModelUser
from src.auth_user.domain.token import JWTToken
from src.auth_user.domain.utils import hashing
from src.auth_user.domain.auth import authorization, Tokens, authentication


class AuthTestCase(TestCase):
    def test_authorization_getting_tokens(self):
        user = ModelUser(
            first_name="firstname1",
            last_name="lastname1",
            patronymic="patronymic1",
            email="email1",
            login="login1",
            password=hashing("password1")
        )
        tokens = authorization(user, "password1")
        self.assertIsInstance(tokens, Tokens)

    def test_authorization_invalid_password_exception(self):
        user = ModelUser(
            first_name="firstname1",
            last_name="lastname1",
            patronymic="patronymic1",
            email="email1",
            login="login1",
            password=hashing("password1")
        )
        self.assertRaises(InvalidPassword, authorization, user, "password2")

    def test_authentication_on_security_data(self):
        user = ModelUser(
            first_name="firstname1",
            last_name="lastname1",
            patronymic="patronymic1",
            email="email1",
            login="login1",
            password=hashing("password1")
        )
        tokens = authorization(user, "password1")
        security_data = tokens.access
        login = authentication(security_data)
        self.assertEqual(login, user.login)

    def test_authentication_invalid_token_exception(self):
        security_data = str(JWTToken("login1", datetime.now(), 0))
        self.assertRaises(InvalidToken, authentication, security_data)
