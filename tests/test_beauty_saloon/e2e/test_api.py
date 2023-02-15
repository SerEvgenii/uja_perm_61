from datetime import datetime, timedelta

from django.test import TestCase

from rest_framework.test import APIClient

from src.core.models import MaterialsByOrder


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
                    "quantity": "4"
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
        response = self.client.post("/api/v1/salon/order/2/", data=data, format='json')
        response_data = response.json()
        self.assertEqual(response_data["profit"], 1060)

    def test_order_query_params(self):
        response = self.client.get("/api/v1/salon/order/?profit>=1000")
        response_data = response.json()
        self.assertEqual(len(response_data), 5)
        response = self.client.get("/api/v1/salon/order/?profit<1000")
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

    def test_orders_of_user(self):
        response = self.client.get("/api/v1/salon/orders-of-user/")
        response_data = response.json()
        self.assertListEqual(response_data["6"], [1, 3, 6])

    def test_top_employee(self):
        response = self.client.get("/api/v1/salon/top-employee/")
        response_data = response.json()
        self.assertDictEqual(response_data[0], {'4': 2900.0})

    def test_orders_per_month(self):
        response = self.client.get("/api/v1/salon/order-per-month/")
        response_data = response.json()
        time = datetime.strptime(response_data[0]["time_input"], '%Y-%m-%dT%H:%M:%S.%f')
        self.assertTrue(time > (datetime.now() - timedelta(days=90)))
