""" Subscription model module """

from django.db import models

class Subscription(models.Model):
    """ Representation of a subscription that a user can create """

    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="author")
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    ended_on = models.DateTimeField(auto_now_add=False, auto_now=False)
