from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareserverapi.models import PostReaction

class PostReactions(ViewSet):
    """postreactions for Rare"""

    def list(self, request):
        "GET post reactions"

        post_reactions = PostReaction.objects.all()

        post = self.request.query_params.get("post_id", None)

        if post is not None:
            post_reactions = post_reactions.filter(post_id=post)

        serializer = PostReactionSerializer(post_reactions, many=True, context={'request': request})

        return Response(serializer.data)

class PostReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostReaction
        fields = ('id', 'post_id', 'reaction_id', 'reactor_id')