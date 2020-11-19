"""Subscriptions Views Module"""
from django.contrib.auth.models import User
from rareserverapi.models import subscription
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareserverapi.models import Subscription, RareUser
from rest_framework.fields import NullBooleanField
from datetime import date
from rest_framework.decorators import action

class Subscriptions(ViewSet):
    """Rare subscriptions"""

    def list(self, request):
        """all subscriptions"""

        subscriptions = Subscription.objects.all()

        follower_id = self.request.query_params.get('user_id', None)
        if follower_id is not None:
            subscriptions = subscriptions.filter(follower_id = follower_id)

        serializer = SubscriptionSerializer(subscriptions, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        new_subscription = Subscription()

        user = RareUser.objects.get(user=request.auth.user)
        new_subscription.follower = user

        new_subscription.author = RareUser.objects.get(pk=request.data["author_id"])
        new_subscription.created_on = date.today()

        new_subscription.save()

        serializer = SubscriptionSerializer(new_subscription, context={'request': request})
        return Response(serializer.data)
    
    @action(methods=['get', 'put'], detail=True)

    def unsubscribe(self, request, pk=None):
        if request.method == 'PUT':

            #define author using pk retrieved from url
            author = RareUser.objects.get(pk=pk)

            #get the subscription object where the author equals the userId (from front end)
            # where follow equals the logged in user
            # and where ended_on === null
            sub = Subscription.objects.get(author=author, follower=request.auth.user.id, ended_on=None)

            #change ended_on to today and save
            sub.ended_on = date.today()
            sub.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('author_id', 'follower_id', 'created_on', 'ended_on')