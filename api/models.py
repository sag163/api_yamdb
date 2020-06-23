from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATUS_CHOICESS = [
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    ]

    username = None
    email = models.EmailField(unique=True)
    confirmation_code = models.IntegerField(blank=True, null=True)
    role = models.CharField(choices=STATUS_CHOICESS, max_length=50, default='user')
    bio = models.CharField(max_length=500, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.
