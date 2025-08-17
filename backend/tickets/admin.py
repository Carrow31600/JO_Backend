from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket_key",
        "order",
        "used",
    )
    list_filter = ("used",)
    search_fields = ("ticket_key", "order__order_key")
