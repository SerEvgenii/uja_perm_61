from rest_framework import routers

from src.beauty_saloon.application_layer.views import DistributionUsersByCategoryView, ServiceView, MaterialView, \
    OrderView

router = routers.SimpleRouter()
router.register(r'roles', DistributionUsersByCategoryView, basename="roles")
router.register(r'services', ServiceView, basename="services")
router.register(r'materials', MaterialView, basename="materials")
router.register(r'order', OrderView, basename="order")
urlpatterns = router.urls
