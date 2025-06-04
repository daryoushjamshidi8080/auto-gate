from django.db import models

# Create your models here.


class antennas(models.Model):
    number = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    open_time = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f'{ self.name } (#{ self.number })'
    
    


