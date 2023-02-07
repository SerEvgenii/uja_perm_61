from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('src.auth_user.entrypoints.urls')),
    path('api/v1/salon/', include('src.beauty_saloon.application_layer.urls')),
]
