from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'lieu', 'sport', 'date') 
    list_filter = ('lieu', 'sport', 'date')         
    search_fields = ('lieu__nom', 'sport__nom')   
    ordering = ('date',)                            
