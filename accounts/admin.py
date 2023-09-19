from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username','role', 'last_login', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
