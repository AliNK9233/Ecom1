from django import forms
from home.models import Variant,Product


class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['color', 'stock', 'price_modifier', 'ram', 'storage', 'battery', 'is_available']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'rating', 'image', 'discount_percentage', 'brand', 'is_available']


