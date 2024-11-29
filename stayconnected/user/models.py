from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

"""

Write log in and registration logics (using django rest framework)

JWT auth

Log in should be by email and password

Registration:

username

email (email verification for future improvement)

password

created at field

status
"""
