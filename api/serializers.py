from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import random

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_code():
    random.seed()
    return str(random.randint(10000000,99999999))

class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("email",)
    
    def validate(self, data):
        confirmation_code = generate_code()
        data['confirmation_code'] = confirmation_code
        return data

class UserAvtorizaytion(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('email', 'confirmation_code',)

    def validate(self, data):
        email = data['email']
        confirmation_code = data['confirmation_code']
        profile = get_object_or_404(User, email=email)
        if profile.confirmation_code != confirmation_code:
            raise ValidationError('ошибка')
        else:
            token = get_tokens_for_user(profile)
            data['token'] = token
        return data
        