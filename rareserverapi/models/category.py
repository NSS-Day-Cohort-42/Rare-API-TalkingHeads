""" Category model module """

from django.db import models

class Category(models.Model):
    """ Representation of a category that a user can create """

    label = models.CharField(max_length=25)
