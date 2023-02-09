from rest_framework.serializers import ModelSerializer, Serializer
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
        employee = User.objects.filter(id=validated_data["id_employee"]).first()
        client = User.objects.filter(id=validated_data["id_client"]).first()
        service = Service.objects.filter(id=validated_data["id_service"]).first()

        try:
            order = Order.objects.create(
                id_employee=employee,
                id_client=client,
                id_service=service
            )
        except IntegrityError:
            raise InvalidData

        dict_materials = {}
        order.profit = service.price
        for obj in validated_data["materials_by_order"]:
            key = obj['id_material']
            if dict_materials.get(key) is None:
                dict_materials[key] = obj['quantity']
                MaterialsByOrder.objects.create(id_order=order, **obj)
                order.profit -= obj["id_material"].price * obj["quantity"]

        order.save()
        return order
