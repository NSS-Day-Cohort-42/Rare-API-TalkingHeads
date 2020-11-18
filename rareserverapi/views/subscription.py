"""PostTags Views Module"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareserverapi.models import PostTag, Tag, Post


class PostTags(ViewSet):
    """Rare post tags"""

    def list(self, request):
        """Handle GET requests to get posttags by post"""

        posttags = PostTag.objects.all()

        #filtering posttags by post
        post = self.request.query_params.get("post_id", None)

        if post is not None:
            posttags = posttags.filter(post_id=post)

        serializer = PostTagSerializer(
            posttags, many=True, context={'request': request})
        return Response(serializer.data)
    def list(self, request):
        """Handle GET requests to get posttags by post"""

        posttags = PostTag.objects.all()

        #filtering posttags by post
        post = self.request.query_params.get("post_id", None)

        if post is not None:
            posttags = posttags.filter(post_id=post)

        serializer = PostTagSerializer(
            posttags, many=True, context={'request': request})
        return Response(serializer.data)    def list(self, request):
        """Handle GET requests to get posttags by post"""

        posttags = PostTag.objects.all()

        #filtering posttags by post
        post = self.request.query_params.get("post_id", None)

        if post is not None:
            posttags = posttags.filter(post_id=post)

        serializer = PostTagSerializer(
            posttags, many=True, context={'request': request})
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations"""

        post = Post.objects.get(pk=request.data["post_id"])
        tag = Tag.objects.get(pk=request.data["tag_id"])

        posttag = PostTag()
        posttag.post = post
        posttag.tag = tag

        try: 
            posttag.save()
            serializer = PostTagSerializer(posttag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single posttag

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            posttag = PostTag.objects.get(pk=pk)
            posttag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PostTag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')


class PostTagSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for posttags"""
    
    tag = TagSerializer(many=False)

    class Meta:
        model = PostTag
        fields = ('id', 'post_id', 'tag_id', 'tag')
        depth = 1