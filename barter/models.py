import datetime
import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
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


class Feedback(models.Model):
    last_edit = models.DateTimeField('Last Edit')
    pub_date = models.DateTimeField('date published')
    message = models.CharField(max_length=200)
    sender = models.ForeignKey(User, related_name='Sender')
    receiver = models.ForeignKey(User, related_name='Receiver')
    rating = models.IntegerField(default=0)

    def edit(self, m):
        self.message = m
        return self


class Favor(models.Model):
    last_edit = models.DateTimeField('Last Edit')
    pub_date = models.DateTimeField('date published')
    message = models.CharField(max_length=200)
    title = models.CharField(max_length=32, default='')
    author = models.ForeignKey(User, related_name='Author')
    completed_by = models.ForeignKey(User, related_name='Completed by', default=None)
    categories = models.CommaSeparatedIntegerField(max_length=16)
    allow_offers = models.BooleanField(default=False)
    status = models.CharField(max_length=16, default='')

    def edit(self, m):
        self.message = m
        return self

