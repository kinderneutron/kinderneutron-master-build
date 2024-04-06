from rest_framework import serializers

class DetectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    result = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
