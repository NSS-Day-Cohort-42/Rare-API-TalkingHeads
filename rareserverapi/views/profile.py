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

class Profiles(ViewSet):
    """ rare user types """
    
    def list(self, request):
        """ Handle GET request for single user profile """

        user = RareUser.objects.get(user=request.auth.user)
        serializer = RareUserSerializer(user, context={'request': request})


        # profile = User.objects.get(pk=pk)
        # serializer = ProfileSerializer(profile, context={'request': request})

        return Response(serializer.data)

        # except Exception as ex:
        #     return HttpResponseServerError(ex)


class ProfileSerializer(serializers.ModelSerializer):
    """ JSON Serializer for profile types

    Arguments:
        serializers
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_staff', 'date_joined')

class RareUserSerializer(serializers.ModelSerializer):
    """ JSON Serializer for user 
    Arguments: 
        serializers
    """
    user = ProfileSerializer(serializers.ModelSerializer)
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'active', 'created_on')