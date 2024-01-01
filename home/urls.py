from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('login_otp/', views.login_otp, name='login_otp'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('product_details/', views.product_details, name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('category/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_stock/', views.admin_stock, name='admin_stock'),
]
