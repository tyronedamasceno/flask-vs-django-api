from django.urls import path, include

from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register('user_register', views.UserViewSet, base_name='user_register')
router.register('user', views.ProtectedUserViewSet, base_name='user')
router.register('login', views.LoginViewSet, base_name='login')

app_name = 'core'

urlpatterns = [
    path('', include(router.urls))
]
