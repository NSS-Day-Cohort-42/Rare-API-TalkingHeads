""" Reaction model module """

from django.db import models

class Reaction(models.Model):
    """ Representation of a reaction that a user can create """

    label = models.CharField(max_length=25)
    image_url = models.URLField()
