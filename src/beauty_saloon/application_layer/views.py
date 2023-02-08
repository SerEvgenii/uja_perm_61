from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from django.forms import model_to_dict

from src.beauty_saloon.common.exceptions import InvalidData
from src.core.models import DistributionUsersByCategory, Service, Material, Order, User, MaterialsByOrder
from src.beauty_saloon.domain_layer.serializers import DistributionUsersByCategorySerializer, \
    ServiceSerializer, MaterialSerializer, OrderSerializer


class DistributionUsersByCategoryView(ModelViewSet):
    queryset = DistributionUsersByCategory.objects.all()
    serializer_class = DistributionUsersByCategorySerializer


class ServiceView(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class MaterialView(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class OrderView(CreateModelMixin,
                RetrieveModelMixin,
                ListModelMixin,
                GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.filter(id=kwargs["pk"]).first()
        employee = User.objects.filter(id=serializer.data["id_employee"]).first()
        client = User.objects.filter(id=serializer.data["id_client"]).first()
        service = Service.objects.filter(id=serializer.data["id_service"]).first()

        if employee and client and service is None:
            raise InvalidData

        order.id_employee = employee
        order.id_client = client
        order.id_service = service
        order.profit = service.price

        materials_by_order_update = set()

        result = {}
        for obj in request.data["materials_by_order"]:
            key = obj['id_material']
            if result.get(key) is None:
                result[key] = obj['quantity']
                material = Material.objects.filter(id=obj["id_material"]).first()
                materials_by_order = MaterialsByOrder.objects.filter(id_order=order, id_material=material).first()
                if materials_by_order:
                    materials_by_order.quantity = obj["quantity"]
                    order.profit -= material.price * int(obj["quantity"])
                    materials_by_order_update.add(materials_by_order)
                else:
                    materials_by_order = MaterialsByOrder.objects.create(
                        id_order=order,
                        id_material=material,
                        quantity=obj["quantity"]
                    )
                    order.profit -= material.price * int(obj["quantity"])
                    materials_by_order_update.add(materials_by_order)

        materials_by_order_all = set(MaterialsByOrder.objects.filter(id_order=order))

        delta = materials_by_order_all - materials_by_order_update

        while delta:
            obj = delta.pop()
            MaterialsByOrder.objects.filter(id=obj.pk).delete()

        order.save()
        return Response(model_to_dict(order))
