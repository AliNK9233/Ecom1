from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

from home.models import Variant

# Create your models here.


    



class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    title = models.TextField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_checkout_done =models.BooleanField(default=False)
    
    @property
    def sub_total(self):
        return Decimal(self.quantity) * self.product.price

    def __str__(self):
        return self.title
