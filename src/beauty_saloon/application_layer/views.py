from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from django.forms import model_to_dict
from rest_framework.views import APIView

from src.beauty_saloon.common.exceptions import InvalidData, InvalidQuery
from src.core.models import DistributionUsersByCategory, Service, Material, Order, User, MaterialsByOrder
from src.beauty_saloon.domain_layer.serializers import DistributionUsersByCategorySerializer, \
    ServiceSerializer, MaterialSerializer, OrderSerializer, OrdersOfUserSerializer


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
        query = self.request.query_params.urlencode()
        if query.count("%3E=") and query.count("profit") == 1:
            try:
                query = query.replace("=", "")
                profit = int(query.split("%3E")[1])
            except ValueError:
                raise InvalidQuery
            return Order.objects.filter(profit__gte=profit)
        if query.count("%3C") and query.count("profit") == 1:
            try:
                query = query.replace("=", "")
                profit = int(query.split("%3C")[1])
            except ValueError:
                raise InvalidQuery
            return Order.objects.filter(profit__lt=profit)

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


class OrdersOfUserView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrdersOfUserSerializer(data=orders, many=True)
        serializer.is_valid()
        for obj in serializer.data:
            print(obj)

        return Response(serializer.data)
