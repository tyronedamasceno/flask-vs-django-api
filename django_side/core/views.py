from django.db import transaction

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from core.models import User
from core.serializers import CustomAuthTokenSerializer, UserSerializer


class ProtectedUserViewSet(mixins.ListModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data={**request.data})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                'token': token.key,
                'user': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


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
