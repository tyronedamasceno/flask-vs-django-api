from datetime import datetime

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    def create(self, **kw):
        return self.create_user(**kw)

    def create_user(self, email, doc_number, password, **kwargs):
        if not email:
            raise ValueError('The Email must be set')
        if not doc_number:
            raise ValueError('The Doc Number must be set')
        user = self.model(
            email=self.normalize_email(email),
            doc_number=doc_number,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, doc_number, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, doc_number, password, **kwargs)



class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    doc_number = models.CharField(max_length=100)
    balance = models.FloatField(default=0.0)

    is_staff = models.BooleanField('Equipe', default=False)  # django user
    is_active = models.BooleanField('Ativo', default=True)  # django user

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['doc_number']

    objects = CustomUserManager()


class Transaction(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
