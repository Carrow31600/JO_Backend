from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'is_staff', 'is_active']
    readonly_fields = ('secret_key',)
  
    fieldsets = UserAdmin.fieldsets + (
        ('Infos supplémentaires', {
            'fields': ('secret_key',)
        }),
    )
    

admin.site.register(CustomUser, CustomUserAdmin)
