import datetime
from django.db import models
from django.contrib.auth import models
from django.utils import timezone


# Create your models here.
class User(models.User):
    DOB = models.DateTimeField('date published')
    feedbacks = models.ManyToManyField(Feedback)

    def get_feedback(self):
        return Feedback.objects.filter(sender=self.id)


class Feedback(models.Model):
    sender = models.ForeignKey(User)
    receiver = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    pubDate = models.DateTimeField('date published')
    message = models.CharField(max_length=200)

    def edit(self,m):
        message = m
        return self


class Favor(models.Model):
    author = models.ForeignKey(User)
    categories = models.ArrayField(models.CharField(max_length=16), size=6)

