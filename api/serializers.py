from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

#User = get_user_model

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", 'password') 
    
    def validate(self, data):
        user = data['username']
        email = data['email']
        profil = get_object_or_404(User, username=user, email=email)
        if profil:
            raise ValidationError()
        return data
    
#    def create(self, validated_data):
#        user = validated_data['username']
#        email = validated_data['email']
#        role = validated_data['role']
#        password = validated_data['password']
#        User.objects.create_user(
#            user=user,
#            email=email,
#            role=role,
#            password=password,
#        )
#        return validated_data
