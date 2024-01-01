from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,related_name="profile")
    phone = models.CharField(max_length=20, unique=True)  # Use phone for login
    age = models.IntegerField()
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  


    def __str__(self):
        return self.phone

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)



class Product(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE) # Assuming a Category model
  price = models.DecimalField(max_digits=10, decimal_places=2)
  rating = models.DecimalField(max_digits=3, decimal_places=1, default=0) # Example rating
  image = models.ImageField(upload_to='product_images') # Example image handling
  discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

  def __str__(self):
    return self.name

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.product} - {self.color}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Relationship to Product model
    image = models.ImageField(upload_to='product_images')

 

