from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('product_details/<int:variant_id>/', views.product_details, name='product_details'),
    
    path('admin_stock/', views.admin_stock, name='admin_stock'),
    
]
