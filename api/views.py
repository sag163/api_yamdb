from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserProfileSerializers
from .models import User
from django.core.mail import send_mail
import random
from rest_framework.response import Response
#from rest_framework import generics
from rest_framework import viewsets
# Create your views here.

def generate_code():
    random.seed()
    return str(random.randint(10000,99999))


class Signup(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializers

    def create(self, request, *args, **kwargs):
        serializer = UserProfileSerializers(data=request.data, context={'request': request})
        if serializer.is_valid(): #raise_exception=True):
            user = serializer.save(comit=False)
            user.confirmation_code = generate_code()
            user.save()
            return Response(user.data)

'''
class Signup(APIView):
    
    def post(self, request):
        serializer = UserProfileSerializers(data=request.POST)
        if serializer.is_valid:
            user = serializer.save(commit=False)
            user.confirmation_code = generate_code()
            user.username = request.user
#            user.password = serializer.cleaned_data['password']
            user.save()

#            serializer.save(username=request.user)
#        user = UserProfile.objects.get(username=request.user)
        if user.is_active == False:
            user.confirmation_code = generate_code()
            send_mail(
                'авторизация',
                f'бла бла {user.confirmation_code}',
                'my@my.my',
                'toto@to.to',
                fail_silently=False,
            )
        return Response(serializer.data)
'''
