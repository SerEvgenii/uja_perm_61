from django.db import models
from django.db.models import Model


class User(Model):
    class Meta:
        db_table = 'user'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)


class UserCategory(Model):
    class Meta:
        db_table = "user_category"

    name = models.CharField(max_length=255)


class DistributionUsersByCategory(Model):
    class Meta:
        db_table = "distribution_users_by_category"

    id_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    id_user_category = models.ForeignKey(to=UserCategory, on_delete=models.CASCADE)
