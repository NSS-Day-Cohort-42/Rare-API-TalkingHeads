from django.urls import path
from rest_framework import routers
from rareserverapi.views import Categories, Posts, register_user, login_user, Tags
from django.conf.urls import include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'posts', Posts, 'post')
router.register(r'tags', Tags, 'tag')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
