from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rareserverapi.models import Comment, Post
from rareserverapi.models import  RareUser

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'commenter_id', 'content', 'subject')


class Comments(ViewSet):
    """comments for rare"""
    def create(self, request):
        """post operations for adding comments"""

        commenter = RareUser.objects.get(user=request.auth.user)

        comment = Comment()

        comment.content = request.data['content']
        comment.subject = request.data['subject']
        comment.created_on = ""

        post = Post.objects.get(pk=request.data["postId"])
        
        comment.commenter = commenter

        comment.post = post

        try:
            comment.save()

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
        """single comment"""
        try:
            comment = Comment.objects.get(pk=pk)

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def list(self, request):
        """all comments"""
        comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

