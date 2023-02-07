from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import IntegerField, CharField, FloatField, ListField, DateTimeField

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
        materials_by_order_data = validated_data.pop("materials_by_order")
        employee = User.objects.filter(id=validated_data["id_employee"]).first()
        client = User.objects.filter(id=validated_data["id_client"]).first()
        service = Service.objects.filter(id=validated_data["id_service"]).first()

        order = Order.objects.create(
            id_employee=employee,
            id_client=client,
            id_service=service
        )
        order.profit = service.price

        for obj in materials_by_order_data:
            MaterialsByOrder.objects.create(id_order=order, **obj)
            order.profit -= obj["id_material"].price * obj["quantity"]

        order.save()
        return order

    def update(self, instance, validated_data):
        print(validated_data)
        employee = User.objects.filter(id=validated_data["id_employee"]).first()
        client = User.objects.filter(id=validated_data["id_client"]).first()
        service = Service.objects.filter(id=validated_data["id_service"]).first()

        instance.id_employee = employee
        instance.id_client = client
        instance.id_service = service
        instance.save()

        materials_by_order_data = validated_data.pop("materials_by_order")

        return instance
