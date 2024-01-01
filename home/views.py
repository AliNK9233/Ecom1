from django.shortcuts import redirect, render
from .models import Category,Variant,UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


#import forms

from .forms import registerForm

# Create your views here.
@login_required(login_url='login')
def index(request):

    dict_cat = {
        'cat':Category.objects.all(),
        'var':Variant.objects.all()
    }
    return render(request,'index.html',dict_cat)

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = registerForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user )
                return redirect('login')  
        else:
            form = registerForm()

        context = {'form': form}
        return render(request, 'signup.html', context)

def user_login(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'User name or password not matching')

    
    context = {}
    return render(request,'login.html',context)

def login_otp(request):
    pass

def user_logout(request):
    logout(request)
    return redirect('login')

def product_details(request):
    return render(request,'product_details.html')

def add_product(request):
    return render(request,'admin_Add_product.html')

def category(request):
    
    dict_category = {
        'catgry':Category.objects.all()
    }

    return render(request,'admin_category.html',dict_category)

def add_category(request):

    return render(request,'admin_category_add.html')

@user_passes_test(lambda u: u.is_staff)
def admin_home(request):
    pass

    # dict_user = {
    #     'user':UserProfile.objects.all()
    # }

    # return render(request,'admin_home.html',dict_user)

def admin_stock(request):

    dict_stock = {
        'stock': Variant.objects.all()
    }

    return render(request,'admin_stock.html',dict_stock)