from django.db import models
from tag.models import Tag
from setting.models import antennas
# Create your models here.


class Logs(models.Model):
    uid = models.CharField(max_length=64)

    status = models.CharField(max_length=64)

    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uid

    class Meta:
        ordering = ["-create_at"]


class Logs(models.Model):
    tag_number = models.IntegerField()
    uid = models.CharField(max_length=64)
    status = models.CharField(max_length=64)
    rule = models.CharField(max_length=128, null=True, blank=True)
    door = models.CharField(max_length=128, null=True, blank=True)
    unit_number = models.CharField(max_length=64, null=True, blank=True)
    car_name = models.CharField(max_length=64, null=True, blank=True)
    owner_name = models.CharField(max_length=128, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uid} - {self.status}"

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "logs"
        verbose_name_plural = "Logs"
