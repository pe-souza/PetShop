from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('apps.admin_panel.urls')),
    path('servicos/', include('apps.services.urls')),
    path('', include('apps.pages.urls')),
]
