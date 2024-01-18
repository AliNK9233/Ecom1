from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('product_details/<int:variant_id>/', views.product_details, name='product_details'),
    path('product_by_category/<int:category_id>/', views.product_by_category, name='product_by_category'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    
    
]
