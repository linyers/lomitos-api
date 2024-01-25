from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LomitosViewSet, lomito_base

router = DefaultRouter()
router.register(r'lomitos', LomitosViewSet, basename="lomito")

app_name = 'api'

urlpatterns = [
    path("", include(router.urls)),
    path("lomito-base/", lomito_base, name="lomito_base")
]
