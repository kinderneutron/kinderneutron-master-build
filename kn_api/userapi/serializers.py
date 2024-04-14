from rest_framework import serializers

class DetectionSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    auth_token = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
