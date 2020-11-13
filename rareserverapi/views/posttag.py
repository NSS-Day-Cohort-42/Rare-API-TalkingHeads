"""PostTags Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareserverapi.models import PostTag, Tag, Post


class PostTags(ViewSet):
    """ Responsible for GET, POST, DELETE """
    def list(self, request):
        """ GET all pt objects """
        posttags = PostTag.objects.all()

        post_id = self.request.query_params.get("postId", None)
        if post_id is not None:
            posttags = posttags.filter(post_id=post_id)

        serializer = PostTagSerializer(posttags, many=True, context={'request', request})
        return Response(serializer.data)

    def create(self, request):
        """ POST """
        #these match the properties in PostForm.js
        post_id = request.data["post_id"]
        tag_id = request.data["tag_id"]

        #check if post exists
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'message: invalid post id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        #check if tag exists
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({'message: invalid tag id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        #check if posttag exists
        try: 
            posttag = PostTag.objects.get(post=post, tag=tag)
            return Response({'message': 'Posttag already exists for these two items'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except PostTag.DoesNotExist:
            #if it does not exist, make new obj
            posttag = PostTag()
            posttag.post = post
            posttag.tag = tag
            try: 
                posttag.save()
                serializer = PostTagSerializer(posttag, many=False, )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ DELETE """
        try:
            posttag = PostTag.objects.get(pk=pk)
            posttag.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except PostTag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostTagSerializer(serializers.ModelSerializer):
    """ Serializes PostTags """
    class Meta:
        model = PostTag
        fields = ('id', 'tag', 'post')
        depth = 1
        #so we can access whole tag and post object