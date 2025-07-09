from django.db import models
from setting.models import antennas
from django.utils import timezone


# Create your models here.


class TagPermission(models.Model):

    permission_name = models.CharField(max_length=255)
    antenna = models.ManyToManyField(
        antennas, related_name="antenna_permissions", blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        antennas = ", ".join([a.name for a in self.antenna.all()])
        return f'{self.permission_name}'


class Tag(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    tag_number = models.IntegerField(unique=True, blank=True, null=True)
    owner_name = models.CharField(max_length=64, blank=True, null=True)
    car_name = models.CharField(max_length=255, blank=True, null=True)
    pelicula = models.CharField(max_length=255, blank=True, null=True)
    number_unit = models.CharField(max_length=255, blank=True, null=True)
    rule = models.ForeignKey(
        TagPermission, on_delete=models.SET_NULL, null=True, related_name="tags_permissions")
    is_active = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner_name } ({self.uid})'
