from django.db import models
from django.contrib.auth.models import User

from home.models import Variant

# Create your models here.


class CartItem(models.Model):
    product_variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product_variant.price * self.quantity

    def __str__(self):
        return f"{self.product_variant.product.name} - {self.product_variant.color} - {self.quantity} units"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='cart_items')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

