from datetime import datetime, timedelta

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from django.forms import model_to_dict
from rest_framework.views import APIView

from src.beauty_saloon.common.exceptions import InvalidData, InvalidQuery
from src.core.models import DistributionUsersByCategory, Service, Material, Order, User, MaterialsByOrder
from src.beauty_saloon.domain_layer.serializers import DistributionUsersByCategorySerializer, \
    ServiceSerializer, MaterialSerializer, OrderSerializer, OrdersOfUserSerializer, ProfitOfOrderSerializer, \
    TopEmployeeSerializer, OrdersPerMonthSerializer


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
        if query.count("profit%3E=") == 1:
            try:
                profit = int(query.split("%3E=")[1])
            except ValueError:
                raise InvalidQuery
            return Order.objects.filter(profit__gte=profit)
        if query.count("profit%3C") == 1:
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

        if (order and employee and client and service) is None:
            raise InvalidData("Invalid data")

        order.id_employee = employee
        order.id_client = client
        order.id_service = service
        order.profit = service.price

        MaterialsByOrder.objects.filter(id_order=order).delete()

        dict_materials = {}
        for obj in serializer.validated_data["materials_by_order"]:
            material = obj["id_material"]
            if dict_materials.get(material) is None:
                dict_materials[material] = obj["quantity"]
                MaterialsByOrder.objects.create(id_order=order, id_material=material, quantity=obj["quantity"])
                order.profit -= material.price * obj["quantity"]
        order.save()
        return Response(model_to_dict(order))


class OrdersOfUserView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrdersOfUserSerializer(data=orders, many=True)
        serializer.is_valid()

        dict_orders_of_user = {}
        for obj in serializer.data:
            key = obj["id_client"]
            if dict_orders_of_user.get(key) is None:
                dict_orders_of_user[key] = [obj["id"]]
            else:
                dict_orders_of_user[key].append(obj["id"])

        return Response(dict_orders_of_user)


class ProfitOfOrderView(ListModelMixin,
                        GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = ProfitOfOrderSerializer


class TopEmployeeView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = TopEmployeeSerializer(data=orders, many=True)
        serializer.is_valid()

        dict_employee = {}
        for obj in serializer.data:
            key = obj["id_employee"]
            if dict_employee.get(key) is None:
                dict_employee[key] = obj["profit"]
            else:
                dict_employee[key] += obj["profit"]

        dict_employee = sorted(dict_employee.items(), key=lambda x: x[1], reverse=True)

        list_top = list()
        for key, value in dict_employee:
            list_top.append({key: value})
        return Response(list_top[:3])


class OrdersPerMonthView(APIView):
    def get(self, request):
        time_limit = datetime.now() - timedelta(days=90)
        orders = Order.objects.filter(time_input__gt=time_limit, profit__gt=1000)
        list_orders = list()
        for order in orders:
            materials_by_order = MaterialsByOrder.objects.filter(id_order=order.pk)
            price = 0
            for obj in materials_by_order:
                price += obj.id_material.price * obj.quantity
            if price < 500:
                list_orders.append(order)

        serializer = OrdersPerMonthSerializer(data=list_orders, many=True)
        serializer.is_valid()

        return Response(serializer.data)
