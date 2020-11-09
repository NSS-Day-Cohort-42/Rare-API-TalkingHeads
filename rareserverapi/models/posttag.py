""" PostTag model module """

from django.db import models

class PostTag(models.Model):
    """ Representation of a post tag that a user can create """

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="tags")
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tags")
