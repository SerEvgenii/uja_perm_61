from rest_framework.test import APITestCase

from src.core.models import User, UserCategory, DistributionUsersByCategory


class ViewTestCase(APITestCase):
    fixtures = ['user.json', 'user_category.json', 'user_by_category.json']
    # @classmethod
    # def setUpTestData(cls):
    #     user = User.objects.create(
    #         first_name="Сергей",
    #         last_name="Сергеев",
    #         patronymic="Сергеевич",
    #         email="sergeev@mail.ru",
    #         login="sergeev",
    #         password="4321"
    #     )
    #     cat = UserCategory.objects.create(name="Клиент")
    #     DistributionUsersByCategory.objects.create(id_user=user, id_user_category=cat)
    #
    # def tearDown(self) -> None:
    #     pass

    def test_distribution_users_by_category(self):
        response = self.client.get("/api/v1/salon/roles/")
        response_data = response.json()
        print(response_data)
        print(response)

    # def test_service(self):
    #     response = self.client.get("/api/v1/salon/services/")
    #     response_data = response.json()
    #     print(response_data)
    #     print(response)
    #
    # def test_material(self):
    #     response = self.client.get("/api/v1/salon/materials/")
    #     response_data = response.json()
    #     print(response_data)
    #     print(response)
