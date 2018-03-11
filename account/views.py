from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import *
from .models import Account
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # Only admin can view the list of users.
    permission_classes = [
        # IsAdminUser
        AllowAny
    ]

class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Token.objects.all()
    serializer_class = AuthTokenSerializer

    permission_classes = [
        # IsAdminUser
        AllowAny
    ]