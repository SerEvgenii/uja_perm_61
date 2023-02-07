from rest_framework.viewsets import ModelViewSet

from src.core.models import DistributionUsersByCategory, Service, Material, Order
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


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
