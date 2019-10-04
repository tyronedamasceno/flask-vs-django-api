from django.db import transaction

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from core.serializers import CustomAuthTokenSerializer, UserSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class LoginViewSet(viewsets.ViewSet):
    @transaction.atomic
    def create(self, request):
        return CustomAuthToken().post(request)
