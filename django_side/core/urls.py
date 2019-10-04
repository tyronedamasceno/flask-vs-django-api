from django.urls import path, include

from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register('login', views.LoginViewSet, base_name='login')

urlpatterns = [
    path('', include(router.urls))
]
