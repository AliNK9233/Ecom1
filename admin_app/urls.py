
from . import views
from django.urls import path


urlpatterns = [

    path('', views.admin_home, name='admin_home'),
    path('user_management/', views.user_management, name='user_management'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'), 
    path('category/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),

    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    path('mark-as-shipped/', views.mark_as_shipped, name='mark_as_shipped'),
    path('mark-as-delivered/', views.mark_as_delivered, name='mark_as_delivered'),
    path('cancel-orders/', views.cancel_orders, name='cancel_orders'),


  
    

    
] 
