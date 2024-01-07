from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)