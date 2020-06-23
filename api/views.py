from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from .serializers import UserSerializers, UserAvtorizaytion
from .models import User
import random
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError



class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.confirmation_code = serializer.validated_data['confirmation_code']
            serializer.email = serializer.validated_data['email']
            serializer.save()
            print(serializer)
            send_mail(
                'Авторизация',
                f'Для авторизации перейдите по ссылке "http://127.0.0.1:8000/api/v1/auth/token/" с параметрами: confirmation_code = {serializer.confirmation_code} email = {serializer.email}',
                'mi@mi.mi',
                [f'{serializer.email}'],
                fail_silently=False,
            )
            return Response(serializer.data)

class Avtorizeytion(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserAvtorizaytion(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'token': serializer.validated_data['token']})

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]
