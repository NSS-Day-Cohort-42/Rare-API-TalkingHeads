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

    def partial_update(self, request, pk=None):
            """update is_staff"""
            user = RareUser.objects.get(user=request.auth.user)
            if user.user.is_staff == True:
                try:
                    user_to_update = RareUser.objects.get(pk=pk)
                    if "is_staff" in request.data:
                        user_to_update.user.is_staff = request.data["is_staff"]
                    else:
                        user_to_update.user.is_active = request.data["is_active"]
                    user_to_update.user.save()
                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                except ValidationError as ex:
                    return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"reason": "Dear hacker, you are not an admin"}, status=status.HTTP_403_FORBIDDEN) 



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff', 'username', 'email', 'is_active')


class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'profile_image_url', 'created_on')


    
    

    
    