"""Tag Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import Tag

class Tags(ViewSet):
    """Tags Class"""

    def list(self, request):
        """ handles GET all"""
        tags = Tag.objects.all()

        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """ handles POST """
        tag = Tag()
        tag.label = request.data["label"]

        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class TagSerializer(serializers.ModelSerializer):
    """ Tag Serializer """
    class Meta:
        model = Tag
        fields = ('id', 'label')