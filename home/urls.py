from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('logout/', views.user_logout, name='logout'),

    path('signup/', views.user_signup, name='signup'),
    

    path('product_details/', views.product_details, name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('category/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),

    path('admin_home/', views.admin_home, name='admin_home'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'), 
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),


    path('admin_stock/', views.admin_stock, name='admin_stock'),
    path('admin_product/', views.admin_product, name='admin_product'),
    path('add_variant/<int:product_id>/', views.add_variant, name='add_variant'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail')
]
