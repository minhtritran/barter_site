from django.contrib import admin
from .models import User, Feedback, Favor


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username', 'first_name', 'last_name', 'password',
         'email', 'DOB', 'is_active', 'groups']}),
        ('Date information', {'fields': ['date_joined', 'last_login'], 'classes': ['collapse']}),
        ('Permissions and User Level', {'fields': ['is_staff', 'user_permissions'], 'classes': ['collapse']}),
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Feedback)
admin.site.register(Favor)