from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


