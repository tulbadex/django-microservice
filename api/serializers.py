from rest_framework import serializers
from .models import TaskResult

class ProcessRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField(max_length=1000)

class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ['email', 'message', 'status', 'result', 'created_at', 'updated_at']
        read_only_fields = fields

class TaskStatusSerializer(serializers.Serializer):
    """Serializer for task status."""

    status = serializers.CharField()
    result = serializers.CharField(allow_null=True)