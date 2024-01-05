from . import views
from django.urls import path
from .views import view_cart

urlpatterns = [

    path('cart/', view_cart, name='view_cart'),
    path('add_to_cart/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    
    
    
    
]
