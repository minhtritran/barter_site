from django.contrib import admin
from .models import User, Feedback, Favor, Offer, Agreement


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username', 'first_name', 'last_name', 'password',
         'email', 'DOB', 'is_active', 'groups']}),
        ('Date information', {'fields': ['date_joined', 'last_login'], 'classes': ['collapse']}),
        ('Permissions and User Level', {'fields': ['is_staff', 'user_permissions'], 'classes': ['collapse']}),
    ]

    list_display = ('username', 'first_name', 'last_name', 'email', 'id')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['last_login', 'date_joined']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'rating', 'pub_date', 'id')
    search_fields = ['sender', 'receiver']
    list_filter = ['pub_date', 'last_edit']


class FavorAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'completed_by', 'pub_date', 'status', 'categories', 'id')
    search_fields = ['sender', 'receiver']
    list_filter = ['pub_date', 'last_edit']


class OfferAdmin(admin.ModelAdmin):
    list_display = ('sender', 'favor', 'pub_date', 'last_edit', 'id')
    search_fields = ['sender', 'favor']
    list_filter = ['pub_date', 'last_edit']


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('sender', 'favor', 'receiver', 'status', 'id')
    search_fields = ['sender', 'receiver']


admin.site.register(User, UserAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Favor, FavorAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Agreement, AgreementAdmin)