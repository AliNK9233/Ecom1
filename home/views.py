from audioop import reverse
import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Category,Variant,UserProfile,Product

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .helper import MessageHandler
from django.shortcuts import render, get_object_or_404

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

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if User.objects.filter(username__iexact=request.POST['username']).exists():
                messages.error(request, "User already exists")
                return redirect('signup')
            
            if form.is_valid():
                user = form.save()

                profile = UserProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data['phone'],
                    age=form.cleaned_data['age'],
                )
                
                user_name = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user_name}')
                return redirect('login')  
        else:
            form = SignupForm()

        context = {'form': form}
        return render(request, 'signup.html', context)

    




# def user_login(request):

#     if request.method == 'POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')

#         user = authenticate(request,username=username,password=password)

#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             messages.info(request,'User name or password not matching')

    
#     context = {}
#     return render(request,'login.html',context)

# def login_otp(request):
#     pass
    
def user_login(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        otp=random.randint(1000,9999)
        

        
        if user is not None:
            
            user_profile = UserProfile.objects.get(user=user)
            phone_number = user_profile.phone
            
            user_profile.otp = otp
            user_profile.save()
            
            messagehandler = MessageHandler(phone_number, otp).send_otp_via_message()
            
            return redirect('otp_verify')
    
              
        else:
            messages.info(request,'User name or password not matching')

    context = {}
    return render(request,'login.html',context)
    
    
def otp_verify(request):
    if request.method == "POST":
        # Perform OTP verification
        profile = UserProfile.objects.get(otp=request.POST['otp'])

        
        if profile.otp == request.POST['otp']:
            user = profile.user
            login(request, user)
 
            return redirect('home')
        return HttpResponse("10 minutes passed")

    return render(request, "login_otp.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def product_details(request):
    return render(request,'product_details.html')

def add_product(request):
    categories = Category.objects.all()  # Fetch categories for the dropdown

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        discount_percentage = request.POST.get('discount_percentage', None)

        try:
            product = Product.objects.create(
                name=name,
                description=description,
                category=Category.objects.get(id=category_id),
                price=price,
                image=image,
                discount_percentage=discount_percentage
            )
            return redirect('product_detail', product.id)  # Redirect to product detail page
        except Exception as e:
            
            print(e)
            return render(request, 'admin_Add_product.html', {'categories': categories, 'error': 'Error creating product'})
    else:
        return render(request, 'admin_Add_product.html', {'categories': categories})

def category(request):
    
    dict_category = {
        'catgry':Category.objects.all()
    }

    return render(request,'admin_category.html',dict_category)

def add_category(request):

    return render(request,'admin_category_add.html')

@user_passes_test(lambda u: u.is_staff)
def admin_home(request):

    dict_user = {
         'userdetails':UserProfile.objects.all(),
         'user':User.objects.all()
    }

    return render(request,'admin_home.html',dict_user)

def admin_stock(request):

    dict_stock = {
        'stock': Variant.objects.all()
    }

    return render(request,'admin_stock.html',dict_stock)

def activate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} has been activated.')
    return redirect('admin_home')  

def deactivate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} has been deactivated.')
    return redirect('admin_home')


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_home')

def admin_product(request):
    products = Product.objects.all()  
    return render(request, 'admin_product.html', {'products': products})

def add_variant(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        color = request.POST.get('color')
        stock = request.POST.get('stock')

        try:
            Variant.objects.create(
                product=product,
                color=color,
                stock=stock
            )
            return redirect('admin_product')  # Redirect to product list
        except Exception as e:
            # Handle errors during variant creation
            print(e)
            return render(request, 'admin_Add_variant.html', {'product': product, 'error': 'Error creating variant'})
    else:
        return render(request, 'admin_Add_variant.html', {'product': product})
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = Variant.objects.filter(product=product)

    context = {
        'product': product,
        'variants': variants,
    }

    return render(request, 'admin_variants.html', context)