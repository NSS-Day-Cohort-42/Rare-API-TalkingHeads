from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareserverapi.models import Reaction


class Reactions(ViewSet):
    """reactions for rare"""

    def list(self, request):
        "GET all reactions"
        reactions = Reaction.objects.all()
        
        serializer = ReactionSerializer(reactions, many=True, context={'request': request})

        return Response(serializer.data)

class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id', 'image_url', 'label')