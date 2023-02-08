from django.db import models
from django.db.models import Model
from django.core.validators import MinValueValidator, MaxValueValidator

from src.core.models import User


class Service(Model):
    class Meta:
        db_table = "service"

    name = models.CharField(max_length=255)
    price = models.FloatField()


class Material(Model):
    class Meta:
        db_table = "material"

    name = models.CharField(max_length=255)
    price = models.FloatField()


class Order(Model):
    class Meta:
        db_table = "order"

    id_employee = models.ForeignKey(to=User, related_name='employee', on_delete=models.PROTECT)
    id_client = models.ForeignKey(to=User, related_name='client', on_delete=models.PROTECT)
    id_service = models.ForeignKey(to=Service, on_delete=models.PROTECT)
    time_input = models.DateTimeField(auto_now_add=True)
    profit = models.FloatField(default=0)


class MaterialsByOrder(Model):
    class Meta:
        db_table = "materials_by_order"

    id_order = models.ForeignKey(to=Order, on_delete=models.PROTECT)
    id_material = models.ForeignKey(to=Material, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
