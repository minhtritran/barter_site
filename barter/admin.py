from django.contrib import admin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Feedback, Favor, Offer, Agreement, Tag

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'gender')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Everything Else', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class TagAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    search_fields = ['slug']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'rating', 'pub_date', 'id')
    search_fields = ['sender', 'receiver']
    list_filter = ['pub_date', 'last_edit']


class FavorAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'status', 'id')
    search_fields = ['author', 'complete_by']
    list_filter = ['pub_date', 'last_edit']


class OfferAdmin(admin.ModelAdmin):
    list_display = ('trader', 'favor', 'pub_date', 'id')
    search_fields = ['trader', 'favor']
    list_filter = ['pub_date', 'last_edit']


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('favor', 'accepter', 'status', 'id')
    search_fields = ['favor', 'accepter']

admin.site.unregister(Group)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Favor, FavorAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Agreement, AgreementAdmin)
