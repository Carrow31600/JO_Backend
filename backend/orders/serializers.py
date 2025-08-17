
from rest_framework import serializers
from .models import OrderLine

class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['id', 'user', 'event', 'offer', 'quantity', 'total_price', 'total_places', 'order_key']
        read_only_fields = ['order_key', 'total_places', 'total_price']
