"""Subscriptions Views Module"""
from rareserverapi.models import subscription
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareserverapi.models import Subscription, RareUser

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

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('author_id', 'follower_id')