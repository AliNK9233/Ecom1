
from django import views
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('products/', include('product_app.urls')),
    path('user/', include('user_app.urls')),
    path('adminapp/', include('admin_app.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
