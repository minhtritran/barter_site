import datetime
import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=30, default=None, blank=True, null=True)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    gender_choices = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=gender_choices, default='m')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        #return self.email
        if self.first_name is None or self.last_name is None:
            return self.email
        else:
            return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        if self.first_name is None:
            return self.email
        else:
            return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def rating(self):
        r = 0
        fb = self.get_feedback()
        for num in fb:
            r += num.rating
        return '{0:.2g}'.format(r/fb.__len__())


class Post(models.Model):
    last_edit = models.DateTimeField('Last Edit', null=True)
    pub_date = models.DateTimeField('Date Published', null=True, default=datetime.datetime.now())
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
    completed_by = models.ForeignKey(User, related_name='Completed by', null=True, default=None)
    categories = models.CommaSeparatedIntegerField(max_length=16)
    allow_offers = models.BooleanField(default=False)
    status = models.CharField(max_length=16, default='open')

    def __str__(self):
        return '"' + self.title + '": ' + self.author.__str__()


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
