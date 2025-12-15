from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('servicos/', include('apps.services.urls')),
    path('', include('apps.pages.urls')),
]
