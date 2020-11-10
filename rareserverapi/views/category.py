""" View module for handling requests for categories """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareserverapi.models import Category

class Categories(ViewSet):
    """ rare category types """

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

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

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