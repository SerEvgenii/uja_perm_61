from rest_framework.viewsets import ModelViewSet

from src.core.models import DistributionUsersByCategory, Service, Material, User
from src.beauty_saloon.application_layer.serializers import DistributionUsersByCategorySerializer, \
    ServiceSerializer, MaterialSerializer, UserSerializers


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class DistributionUsersByCategoryView(ModelViewSet):
    queryset = DistributionUsersByCategory.objects.all()
    serializer_class = DistributionUsersByCategorySerializer


class ServiceView(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class MaterialView(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
