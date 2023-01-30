# from django.db import models
# from django.db.models import Model
#
#
# class User(Model):
#     class Meta:
#         db_table = 'user'
#
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     patronymic = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, unique=True)
#     login = models.CharField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
