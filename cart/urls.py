from . import views
from django.urls import path
from .views import view_cart

urlpatterns = [

    path('cart/', view_cart, name='view_cart'),
    path('add_to_cart/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase_quantity/<int:cart_item_id>/',views. increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    
    
    
]
