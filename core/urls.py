from django.urls import path, include

urlpatterns = [
    path('admin-panel/', include('apps.admin_panel.urls')),
    path('servicos/', include('apps.services.urls')),
    path('', include('apps.pages.urls')),
]
