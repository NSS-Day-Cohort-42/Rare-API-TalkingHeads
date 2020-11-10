from django.urls import path
from rest_framework import routers
from rareserverapi.views import Categories
from django.conf.urls import include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
