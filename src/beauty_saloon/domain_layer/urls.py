from rest_framework import routers

from .views import DistributionUsersByCategoryView, ServiceView, MaterialView, UserView

router = routers.SimpleRouter()
router.register(r'user', UserView, basename="user")
router.register(r'roles', DistributionUsersByCategoryView, basename="roles")
router.register(r'services', ServiceView, basename="services")
router.register(r'materials', MaterialView, basename="materials")
urlpatterns = router.urls
