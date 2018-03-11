from .models import Account
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authentication import BaseAuthentication
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from pdb import set_trace


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password', 'username',)

    def create(self, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        user = get_user_model().objects.create(**validated_data)
        return user


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user',)
        depth = 2

    def validate(self, data):
        print(data['user'])
        email = data['user'].email
        password = data.get('password')

        if email and password:
            user = BaseAuthentication.authenticate(email=email, password=password)

            if user:
                msg = _("User account is disabled.")
                raise ValidationError(msg)

        else:
            msg = _("Must include email and password.")
            raise ValidationError(msg)

        data['user'] = user
        return data
