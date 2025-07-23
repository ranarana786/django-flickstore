from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

class MyAccount(UserAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'username',
        'last_login',
        'date_joined',
        'is_admin',
        'is_active',
        'is_superadmin'
    )
    readonly_fields = (
        'date_joined',
        'last_login'
    )

    ordering = ('-date_joined',)

    list_display_links = (
        'email','username'
    )

    filter_horizontal = ()
    fieldsets = ()
    list_filter = ()

admin.site.register(Account, MyAccount)