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

    def get_queryset(self):
        profit = self.request.query_params
        # queryset = Order.objects.filter(profit__gt=profit)
        # queryset = Order.objects.filter(profit__lt=profit)
        print(self.request.query_params)
        queryset = Order.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.filter(id=kwargs["pk"]).first()
        employee = User.objects.filter(id=serializer.data["id_employee"]).first()
        client = User.objects.filter(id=serializer.data["id_client"]).first()
        service = Service.objects.filter(id=serializer.data["id_service"]).first()

        if order and employee and client and service is None:
            raise InvalidData

        order.id_employee = employee
        order.id_client = client
        order.id_service = service
        order.profit = service.price

        MaterialsByOrder.objects.filter(id_order=order).delete()

        dict_materials = {}
        for obj in request.data["materials_by_order"]:
            key = obj['id_material']
            if dict_materials.get(key) is None:
                dict_materials[key] = obj['quantity']
                material = Material.objects.filter(id=key).first()
                MaterialsByOrder.objects.create(id_order=order, id_material=material, quantity=obj["quantity"])
                order.profit -= material.price * int(obj["quantity"])

        order.save()
        return Response(model_to_dict(order))
