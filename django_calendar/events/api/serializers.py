from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Event

class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'start_at', 'period']
        read_only_fields = ['id']

    def validate_period(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Period cannot be negative.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)