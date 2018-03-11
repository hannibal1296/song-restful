from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'account-list', views.AccountViewSet, 'account-list')
router.register(r'token-list', views.TokenViewSet, 'token-list')

# 127.0.0.1:8000/account/
urlpatterns = [
    path('', include(router.urls)),
]