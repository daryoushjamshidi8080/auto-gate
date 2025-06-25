from django.db import models
# from django.utils import timezone
# Create your models here.


class AnonymousTag(models.Model):
    uid_anonymousTag = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Anonymous Tag : {self.uid_anonymousTag} id {self.id}  / time : {self.create_at}'
