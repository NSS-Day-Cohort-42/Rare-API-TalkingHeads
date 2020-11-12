""" View module for handling requests for categories """
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareserverapi.models import Category

class Categories(ViewSet):
    """ rare category types """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response indicating success of request
        """
        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Handle Get requests for a single category type
        Returns: 
            Response -- JSON serialized category type
    """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """ Handle GET requests to get all categories 
        Returns:
            Response -- JSON serialized list of category types
        """
        categories = Category.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handles DELETE resquests for a category
        Returns:
            Response indicating success (200, 404 or 500 status code)
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """ JSON Serializer for category types 
    Arguments: 
        serializers
    """
    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='category',
            lookup_field='id'
        )
        fields = ('id', 'label')