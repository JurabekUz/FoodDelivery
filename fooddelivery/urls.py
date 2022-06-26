from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('',include('customers.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
