from . import views
from django.urls import path

urlpatterns = [


    
    path('login/', views.user_login, name='login'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    


]
