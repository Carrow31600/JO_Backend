from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'lieu', 'sport', 'date']

def get_event_name(self, obj):
        return f"{obj.event.sport} - {obj.event.lieu} - {obj.event.date}"