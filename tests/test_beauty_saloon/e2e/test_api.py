from django.test import TestCase

from rest_framework.test import APIClient

from src.core.models import MaterialsByOrder, Order


class ViewTestCase(TestCase):
    client_class = APIClient
    fixtures = [
        'user.json',
        'user_category.json',
        'users_by_category.json',
        'service.json',
        'material.json',
        'order.json',
        'materials_by_order.json',
    ]

    def test_distribution_users_by_category(self):
        response = self.client.get("/api/v1/salon/roles/")
        self.assertEqual(response.status_code, 200)

    def test_service(self):
        response = self.client.get("/api/v1/salon/services/")
        self.assertEqual(response.status_code, 200)

    def test_material(self):
        response = self.client.get("/api/v1/salon/materials/")
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        data = {
            "id_employee": "1",
            "id_client": "1",
            "id_service": "2",
            "materials_by_order": [
                {
                    "id_material": "2",
                    "quantity": "2"
                },
                {
                    "id_material": "3",
                    "quantity": "2"
                },
                {
                    "id_material": "3",
                    "quantity": "2"
                }
            ]
        }
        response = self.client.post("/api/v1/salon/order/", data=data, format='json')
        response_data = response.json()
        self.assertEqual(response_data["profit"], 1030)

    def test_update_order(self):
        data = {
            "id_employee": "2",
            "id_client": "1",
            "id_service": "4",
            "materials_by_order": [
                {
                    "id_material": "1",
                    "quantity": "3"
                },
                {
                    "id_material": "4",
                    "quantity": "2"
                },
                {
                    "id_material": "2",
                    "quantity": "4"
                },
                {
                    "id_material": "2",
                    "quantity": "2"
                }
            ]
        }
        response = self.client.post("/api/v1/salon/order/1/", data=data, format='json')
        response_data = response.json()
        self.assertEqual(response_data["profit"], 1060)


