from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from back.models.base import LocationModel
from back.models.city import City
from django.contrib.gis.db import models as geomodel


class FactoryType(models.Model):
    name = models.CharField(max_length=200)
    danger_class = models.IntegerField(default=1)


class Factory(TimeStampedModel, LocationModel):
    name = geomodel.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='factory')

    polygon = geomodel.MultiPolygonField("Perimetr", blank=True, null=True)

    factory_type = models.ForeignKey(FactoryType, on_delete=models.SET_NULL, null=True, related_name='factory')

    danger_score = models.FloatField(default=0, max_length=1)  # условный вред от 1 до 10

    photo = models.ImageField(null=True, blank=True)
    icon = models.FileField(null=True, blank=True)
