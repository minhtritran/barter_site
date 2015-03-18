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

    def __str__(self):
        return self.username + ' (' + self.last_name + ', ' + self.first_name + ')'


class Post(models.Model):
    last_edit = models.DateTimeField('Last Edit', null=True)
    pub_date = models.DateTimeField('Date Published', null=True)
    message = models.CharField(max_length=200, default='')

    def edit(self, m):
        self.message = m
        last_edit = datetime.datetime.now()
        return self

    class Meta:
        abstract = True


class Feedback(Post):
    sender = models.ForeignKey(User, related_name='Feedback Sender')
    receiver = models.ForeignKey(User, related_name='Feedback Receiver')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.sender.__str__() + ' ' + str(self.rating)


class Favor(Post):
    title = models.CharField(max_length=32, default='')
    author = models.ForeignKey(User, related_name='Author')
    completed_by = models.ForeignKey(User, related_name='Completed by', default=None)
    categories = models.CommaSeparatedIntegerField(max_length=16)
    allow_offers = models.BooleanField(default=False)
    status = models.CharField(max_length=16, default='open')

    def __str__(self):
        return '"' + self.title + '": ' + self.sender.__str__()


class Offer(Post):
    favor = models.ForeignKey(Favor, related_name='Offers Favor')
    sender = models.ForeignKey(User)

    def __str__(self):
        return '"' + self.sender.__str__() + '"'


class Agreement(models.Model):
    sender = models.ForeignKey(User, related_name='Agreement Sender', null=True)
    favor = models.ForeignKey(Favor, related_name='Agreement Favor', null=True)
    receiver = models.ForeignKey(User, related_name='Agreement Receiver', null=True)
    status = models.CharField(max_length=16, default='pending')
    customOffer = models.ForeignKey(Offer, null=True)

    def __str__(self):
        return self.sender.__str__() + ' (' + self.status + ')'