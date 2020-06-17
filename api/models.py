from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATUS_CHOICESS = [
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    ]
    confirmation_code = models.IntegerField(blank=True, null=True) #, write_only=True)
    is_active = models.BooleanField(default=False)
    role = models.CharField(choices=STATUS_CHOICESS, max_length=50, default='user')


