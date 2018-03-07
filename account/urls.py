from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'list', views.AccountViewSet, 'list')

# 127.0.0.1:8000/account/
urlpatterns = [
    path('', include(router.urls)),
]