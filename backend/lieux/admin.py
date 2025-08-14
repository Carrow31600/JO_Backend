from django.contrib import admin
from .models import Lieu

@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'code_postal')
    search_fields = ('nom', 'ville', 'code_postal')
