import datetime
import django.contrib.auth.models
from django.db import models
from django.utils import timezone


# Create your models here.
class User(django.contrib.auth.models.User):
    DOB = models.DateField('Date of Birth')

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'email']

    def get_feedback(self):
        return Feedback.objects.filter(sender=self.id)

    def get_favors_completed(self):
        return Favor.objects.filter(status='complete', completed_by=self.id)


class Post(models.Model):
    last_edit = models.DateTimeField('Last Edit', default=datetime.timedelta())
    pub_date = models.DateTimeField('date published')
    message = models.CharField(max_length=200)

    def edit(self, m):
        self.message = m
        return self

    class Meta:
        abstract = True


class Feedback(Post):
    sender = models.ForeignKey(User, related_name='Sender')
    receiver = models.ForeignKey(User, related_name='Receiver')
    rating = models.IntegerField(default=0)


class Favor(Post):
    title = models.CharField(max_length=32, default='')
    author = models.ForeignKey(User, related_name='Author')
    completed_by = models.ForeignKey(User, related_name='Completed by', default=None)
    categories = models.CommaSeparatedIntegerField(max_length=16)
    allow_offers = models.BooleanField(default=False)
    status = models.CharField(max_length=16, default='')

