from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

#User = get_user_model

class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", 'role') 