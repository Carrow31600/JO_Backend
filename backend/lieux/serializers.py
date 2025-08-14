from rest_framework import serializers
from .models import Lieu

class LieuSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()  #url complète de la photo

    class Meta:
        model = Lieu
        fields = ['id', 'nom', 'description', 'photo_url', 'code_postal', 'ville']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None
