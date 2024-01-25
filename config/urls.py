from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import home, get_routes

adminpath = 'admin/'
if not settings.DEBUG:
    adminpath = settings.ADMIN_URL

urlpatterns = [
    path(adminpath, admin.site.urls),
    path("", home, name="home"),
    path("api/", get_routes, name="routes"),
    path('api/', include('api.urls', namespace='api')),
    path('api/auth/', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)