from django.contrib import admin
from .models import  Sport

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
