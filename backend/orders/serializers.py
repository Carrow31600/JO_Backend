from rest_framework import serializers
from .models import OrderLine

class OrderLineSerializer(serializers.ModelSerializer):
    event_name = serializers.SerializerMethodField()
    offer_name = serializers.CharField(source="offer.nom", read_only=True)

    class Meta:
        model = OrderLine
        fields = [
            'id',
            'user',
            'event',
            'event_name',
            'offer',
            'offer_name',
            'quantity',
            'total_price',
            'total_places',
            'order_key'
        ]
        read_only_fields = ['order_key', 'total_places', 'total_price']

    def get_event_name(self, obj):
        # Concatène sport + lieu + date
        return f"{obj.event.sport} - {obj.event.lieu} - {obj.event.date}"
    

