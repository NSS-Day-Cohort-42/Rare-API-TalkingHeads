""" Comment model module """

from django.db import models

class Comment(models.Model):
    """ Representation of a comment that a user can create """

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    commenter = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    subject = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    @property
    def is_owner(self):
        return self.__is_owner

    @is_owner.setter
    def is_owner(self, value):
        self.__is_owner = value
