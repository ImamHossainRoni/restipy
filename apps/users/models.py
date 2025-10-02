import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from core.models import BaseModel
from .managers import CustomUserManager


class User(BaseModel, AbstractUser):
    """
    User Model: Represents a user with authentication and profile attributes.
    """
    username = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True, help_text='User personal unique email')
    # Authentication
    last_pass_change = models.DateTimeField(default=datetime.now)
    forgot_password = models.BooleanField(default=False)
    user_ip = models.CharField(default='', max_length=128)
    auth_token = models.CharField(max_length=64, null=True)
    two_factor = models.BooleanField(default=False, help_text='Activates two factor auth')
    access_expiration_delta = models.PositiveSmallIntegerField(default=600,
                                                               validators=[MaxValueValidator(3600),
                                                                           MinValueValidator(300)]
                                                               , help_text='Auto logout on activity.')

    profile_picture = models.ImageField(null=True,
                                        blank=True,
                                        upload_to='profile_pictures/',)

    is_authority = models.BooleanField(default=False, help_text="Ture If user has authority power else False")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
        ]

    @property
    def name(self):
        return "{0} {1}".format(self.first_name, self.last_name)