from rest_framework import serializers

class ErrorLogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    error_type = serializers.CharField(max_length=200)
    message = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
