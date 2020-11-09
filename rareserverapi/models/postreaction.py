""" PostReaction model module """

from django.db import models

class PostReaction(models.Model):
    """ Representation of a post reaction that a user can create """

    reactor = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="reactions")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reactions")
