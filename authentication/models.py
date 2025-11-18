from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)
    deletedat = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True, name='active')

