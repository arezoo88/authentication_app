from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile_number, password, **extra_fields):
        """
        Create and save a user with the given mobile_number and password.
        """
        if not mobile_number:
            raise ValueError('The given mobile_number must be set')
        mobile_number = self.normalize_mobile_number(mobile_number)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile_number, password, **extra_fields)

    def create_superuser(self, mobile_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(mobile_number, password, **extra_fields)

    def normalize_mobile_number(self, mobile_number):
        return mobile_number


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    mobile_regex = RegexValidator(
        regex=r'09(\d{9})$', message="Enter a valid mobile number. This value may contain only numbers.")
    mobile_number = models.CharField(
        verbose_name=_("Mobile Number"),
        validators=[mobile_regex],
        max_length=11,
        unique=True,
        error_messages={'unique': _('A user with that mobile_number already exists.')})

    objects = UserManager()

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile_number
