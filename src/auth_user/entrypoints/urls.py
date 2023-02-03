from django.urls import path

from .views import UserView, AuthorizationView

urlpatterns = [
    path('account/', UserView.as_view(), name='Account'),
    path('security/', AuthorizationView.as_view(), name='Security Token'),
]
