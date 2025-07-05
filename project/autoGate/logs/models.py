from django.db import models
from tag.models import Tag
# Create your models here.


class Logs(models.Model):
    uid = models.CharField(max_length=64)
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="tag_logs")
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uid

    class Meta:
        ordering = ["-create_at"]
