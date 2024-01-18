from . import views
from django.urls import path

urlpatterns = [
    path('order_list/', views.order_list, name='order_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_tracking/<int:order_id>/', views.order_tracking, name='order_tracking'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('change_address/<int:order_id>/', views.change_address, name='change_address'),
    path('order_invoice/<int:order_id>/', views.order_invoice, name='order_invoice'),
    
]
