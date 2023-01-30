from django.test import TestCase

from src.auth_user.domain.authorization import ModelUser, Authorization, JWTToken


class AuthorizationTestCase(TestCase):
    def test_authorization_getting_jwt_token(self):
        user = ModelUser(
            first_name="firstname1",
            last_name="lastname1",
            patronymic="patronymic1",
            email="email1",
            login="login1",
            password="hash1"
        )

        auth = Authorization(user, 'hash1')
        jwt_token = auth.get_jwt_token()
        self.assertIsInstance(jwt_token, JWTToken)
