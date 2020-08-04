from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminChangeForm, UserAdminCreationForm

# User model
User = get_user_model()


# Customizing the interface of User model in the Admin Page
class UserAdmin(BaseUserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'username', 'is_active', 'is_staff', 'is_admin']
    list_filter = ['username']

    fieldsets = [
        [None, {'fields': ['email', 'password', ]}],
        ['Personal Info', {'fields': ['username', ]}],
        ['Permissions', {'fields': ['is_active', 'is_staff', 'is_admin']}],
    ]

    add_fieldsets = [
        [
            None,
            {
                'classes': ['wide', ],
                'fields': ['username', 'email', 'password', 'confirm_password'],
            },
        ],
    ]

    search_fields = ['username', 'email', ]
    ordering = ['username', ]
    filter_horizontal = []


# Registering User model and its interface in admin page
admin.site.register(User, UserAdmin)
