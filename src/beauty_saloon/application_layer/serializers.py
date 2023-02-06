from rest_framework.serializers import ModelSerializer

from src.core.models import DistributionUsersByCategory, Service, Material, User


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


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
