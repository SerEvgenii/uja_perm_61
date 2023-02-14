from rest_framework import routers
from django.urls import path

from src.beauty_saloon.application_layer.views import DistributionUsersByCategoryView, ServiceView, MaterialView, \
    OrderView, OrdersOfUserView, ProfitOfOrderView, TopEmployeeView, OrdersPerMonthView

router = routers.SimpleRouter()
router.register(r'roles', DistributionUsersByCategoryView, basename="roles")
router.register(r'services', ServiceView, basename="services")
router.register(r'materials', MaterialView, basename="materials")
router.register(r'order', OrderView, basename="order")

urlpatterns = [
    path('orders-of-user/', OrdersOfUserView.as_view(), name='orders_of_user'),
    path('profit-of-order/', ProfitOfOrderView.as_view(), name='profit_of_order'),
    path('top-employee/', TopEmployeeView.as_view(), name='top_employee'),
    path('order-per-month/', OrdersPerMonthView.as_view(), name='order_per_month'),
]
urlpatterns += router.urls
