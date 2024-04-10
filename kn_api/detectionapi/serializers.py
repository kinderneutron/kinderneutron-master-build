from rest_framework import serializers

class DetectionSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    timestamp = serializers.DateTimeField()
    result = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
