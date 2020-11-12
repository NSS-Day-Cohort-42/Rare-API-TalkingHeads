""" View module for handling requests for categories """

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
        post.approved = request.data["approved"]
        post.author = author

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

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = posts.filter(author_id=user_id)

            for post in posts:
                post.is_owner = False
                if post.author.id == current_user.id:
                    post.is_owner = True


        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

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
        fields = ('id', 'author', 'category', 'title', 'image_url', 'publication_date', 'content', 'approved', 'is_owner')
        depth = 1