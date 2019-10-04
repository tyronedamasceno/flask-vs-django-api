from django.core import exceptions
from django.contrib.auth import authenticate

from rest_framework import serializers

from core.models import User, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email, doc_number', 'balance', 'password')
        extra_kwargs = {
            'balance': {'read_only': True},
            'password': {'write_only': True}
        }


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'timestamp', 'value', 'user_id')


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data
