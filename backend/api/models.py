from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BackendUser(AbstractUser):
    isadmin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Item(models.Model):
    user = models.ForeignKey(BackendUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=128) 
    price = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name