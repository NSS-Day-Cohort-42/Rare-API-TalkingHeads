""" Demotion queue model module """

from django.db import models

class DemotionQueue(models.Model):
    """ Representation of a DemotionQueue join table """

    action = models.CharField(max_length=125)
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="demoter")
    approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="demoter_one")
