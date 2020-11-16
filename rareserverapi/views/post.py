""" View module for handling requests for categories """

from rest_framework.status import HTTP_404_NOT_FOUND
from rareserverapi.models.category import Category
from rest_framework import status
from rareserverapi.models.rareuser import RareUser
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareserverapi.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 

class Posts(ViewSet):
    """ rare Post  """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response indicating success of request
        """

        post = Post()
        category = Category.objects.get(pk=request.data["category_id"])
        author = RareUser.objects.get(user=request.auth.user)
        post.category = category
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.author = author
        post.approved = request.data["approved"]
        try:
            # user_admin = User.objects.get(request.auth.user)
            
            if author.user.is_staff == True:
                post.approved = True
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
            
                

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Handle Get requests for a single post
        Returns: 
            Response -- JSON serialized post
    """
        try:
            post = Post.objects.get(pk=pk)
            current_user = RareUser.objects.get(user=request.auth.user)

            post.is_owner = False
            if post.author_id == current_user.id:
                post.is_owner = True

            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """ Handle GET requests to get all posts 
        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        current_user = RareUser.objects.get(user=request.auth.user)

        for post in posts:
            post.is_owner = False
            if post.author_id == current_user.id:
                post.is_owner = True

        current_user = RareUser.objects.get(user=request.auth.user)

        for post in posts:
            post.is_owner = None
            if post.author_id == current_user.id:
                post.is_owner = True
            else:
                post.is_owner = False

        # if pk == "myposts":
        #     pk = current_user.id
        #     posts = posts.filter(author_id = pk)

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = posts.filter(author_id=user_id)

            


        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """edits post"""

        post = Post.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category_id"])
        author = RareUser.objects.get(user=request.auth.user)
        post.category = category
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        # post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.author = author

        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handles DELETE resquests for a post
        Returns:
            Response indicating success (200, 404 or 500 status code)
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSerializer(serializers.ModelSerializer):
    """ JSON Serializer for user 
    Arguments: 
        serializers
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class RareUserSerializer(serializers.ModelSerializer):
    """ JSON Serializer for user 
    Arguments: 
        serializers
    """
    user = UserSerializer(serializers.ModelSerializer)
    class Meta:
        model = RareUser
        fields = ('id', 'user')

class PostSerializer(serializers.ModelSerializer):
    """ JSON Serializer for post 
    Arguments: 
        serializers
    """
    author = RareUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 'image_url', 'publication_date', 'content', 'approved', 'is_owner', 'author_id', 'category_id')
        depth = 1