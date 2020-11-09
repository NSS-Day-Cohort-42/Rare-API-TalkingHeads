""" RareUser model module """

from django.db import models
from django.conf import settings

class RareUser(models.Model):
    """ Representation of a rare user account that a user can create """

    bio = models.CharField(max_length=250)
    profile_image_url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
