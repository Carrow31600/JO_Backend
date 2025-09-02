from django.contrib import admin
from .models import OrderLine

@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "event",
        "offer",
        "quantity",
        "total_price",
        "total_places",
        "order_key",
    )
    search_fields = ("user__username", "event__sport__nom", "offer__nom")
    list_filter = ("event", "offer")

    readonly_fields = ("order_key",)