from django.urls import path

from src.auth_user.entrypoints.views import UserView, SecurityToken

urlpatterns = [
    path('account/', UserView.as_view(), name='Account'),
    path('security/token/', SecurityToken.as_view(), name='Security Token'),
]
