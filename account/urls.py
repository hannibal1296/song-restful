from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'account-list', views.AccountViewSet, 'account-list')
router.register(r'token-list', views.TokenViewSet, 'token-list')

# 127.0.0.1:8000/account/~
urlpatterns = [
    path('', include(router.urls)),
]


'''
1. How to add an account test:
    http POST :8000/account/account-list/ email={your_email} password={your_password} username={your_username}
2. How to retrieve token key:
    http --form POST :8000/api-token-auth/ username={username} password={password}
'''
#