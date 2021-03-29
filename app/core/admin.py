from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin): # extend default django UserAdmin
    # list email, name and order by id
    ordering = ['id']
    list_display = ['email', 'name']


# register UserAdmin(admin page) to our custom User model
admin.site.register(models.User, UserAdmin) 

