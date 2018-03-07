from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import AccountSerializer
from .models import Account
from rest_framework.permissions import IsAuthenticated


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # Only admin can view the list of users.
    permission_classes = [
        IsAuthenticated
    ]
