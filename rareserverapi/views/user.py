from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rareserverapi.models import RareUser

class Users(ViewSet):

    def list(self, request):
        """view all users"""
        try:
            users = RareUser.objects.all()

            serializer = RareUserSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def retrieve(self, request, pk=None):
        """single user"""
        try:
            user = RareUser.objects.get(pk=pk)

            serializer = RareUserSerializer(user, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff', 'username')


class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'profile_image_url')


    
    

    
    