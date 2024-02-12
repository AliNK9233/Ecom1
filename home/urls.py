from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('product_details/<int:variant_id>/', views.product_details, name='product_details'),
    path('product_by_category/<int:category_id>/', views.product_by_category, name='product_by_category'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update-payment-status/', views.update_payment_status, name='update_payment_status'),

    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase_quantity/<int:cart_item_id>/',views.increase_quantity, name='increase_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
]
