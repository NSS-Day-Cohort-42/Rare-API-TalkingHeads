""" Tag model module """

from django.db import models

class Tag(models.Model):
    """ Representation of a tag that a user can create """

    label = models.CharField(max_length=25)
