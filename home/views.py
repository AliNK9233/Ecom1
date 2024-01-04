
from django.shortcuts import redirect, render
from .models import Category,Variant
from django.shortcuts import render

#import forms

from .forms import SignupForm

# Create your views here.
#@login_required(login_url='login')
def index(request):

    dict_cat = {
        'cat':Category.objects.all(),
        'var':Variant.objects.all()
    }
    return render(request,'index.html',dict_cat)


def product_details(request):
    return render(request,'product_details.html')


def admin_stock(request):

    dict_stock = {
        'stock': Variant.objects.all()
    }

    return render(request,'admin_stock.html',dict_stock)



    
