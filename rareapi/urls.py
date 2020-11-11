from django.urls import path
from rest_framework import routers
from rareserverapi.views import Categories, register_user, login_user, Comments
from django.conf.urls import include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'comments', Comments, 'comment')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
