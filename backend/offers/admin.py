from django.contrib import admin
from .models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_places', 'prix')
    search_fields = ('nom',)
    ordering = ('nom',)
