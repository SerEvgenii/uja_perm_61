from rest_framework.serializers import ModelSerializer, Serializer, ValidationError
from rest_framework.fields import CharField, FloatField, ListField
from django.db.utils import IntegrityError

from src.beauty_saloon.common.exceptions import InvalidData
from src.core.models import DistributionUsersByCategory, Service, Material, MaterialsByOrder, Order, User


class DistributionUsersByCategorySerializer(ModelSerializer):
    class Meta:
        model = DistributionUsersByCategory
        fields = ("id_user", "id_user_category")


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class MaterialsByOrderSerializer(ModelSerializer):
    class Meta:
        model = MaterialsByOrder
        fields = ("id_material", "quantity")


class OrderSerializer(Serializer):
    materials_by_order = ListField(child=MaterialsByOrderSerializer(), write_only=True)
    id_employee = CharField()
    id_client = CharField()
    id_service = CharField()
    profit = FloatField(default=0)

    def create(self, validated_data):
        try:
            order = Order.objects.create(
                id_employee=User.objects.filter(id=validated_data["id_employee"]).first(),
                id_client=User.objects.filter(id=validated_data["id_client"]).first(),
                id_service=Service.objects.filter(id=validated_data["id_service"]).first(),
                profit=Service.objects.filter(id=validated_data["id_service"]).first().price
            )
        except IntegrityError:
            raise InvalidData("Invalid data")

        dict_materials = {}
        for obj in validated_data["materials_by_order"]:
            key = obj['id_material']
            if dict_materials.get(key) is None:
                dict_materials[key] = obj['quantity']
                MaterialsByOrder.objects.create(id_order=order, **obj)
                order.profit -= obj["id_material"].price * obj["quantity"]

        order.save()
        return order


class OrdersOfUserSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "id_client")


class ProfitOfOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "profit")


class TopEmployeeSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id_employee", "profit")


class OrdersPerMonthSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
