from calliope_web.models import Bss
from rest_framework import serializers

class BssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bss
        fields = ('author', 'body', 'created_at', 'updateded_at')