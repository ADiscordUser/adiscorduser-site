from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.core.validators import MinLengthValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, validators=[MinLengthValidator(3)], unique=True, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.normalize_username(self.username)

@receiver(models.signals.post_save, sender=User)
def create_api_key(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)