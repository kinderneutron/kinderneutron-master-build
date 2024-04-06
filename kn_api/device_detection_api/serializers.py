from rest_framework import serializers

class DeviceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
    device_name = serializers.CharField(max_length=255)
    login_time = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()