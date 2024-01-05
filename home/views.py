
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category,Variant,Product
from django.shortcuts import render

#import forms

from .forms import SignupForm

# Create your views here.

def index(request):

    dict_cat = {
        'category':Category.objects.all(),
        'variants':Variant.objects.all()
    }
    return render(request,'index.html',dict_cat)


def product_details(request, variant_id):
    variant = get_object_or_404(Variant, pk=variant_id)
    product = variant.product
    variants = product.variant_set.all()
    return render(request, 'product_details.html', {'variant': variant, 'variants': variants, 'selected_variant': variant})


def admin_stock(request):

    dict_stock = {
        'stock': Variant.objects.all()
    }

    return render(request,'admin_stock.html',dict_stock)



    
