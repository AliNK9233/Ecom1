from django.shortcuts import render
from audioop import reverse
import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from home.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from home.helper import MessageHandler
from django.shortcuts import render, get_object_or_404

#import forms

from home.forms import SignupForm

    
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
