from calliope_web.models import Bss, CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'date_joined')

class BssSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    class Meta:
        model = Bss
        fields = ('author', 'body', 'created_at', 'updated_at')
