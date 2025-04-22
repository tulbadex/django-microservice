from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProcessRequestSerializer, TaskResultSerializer, TaskStatusSerializer
from .tasks import process_message
from .models import TaskResult
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

class ProcessView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=ProcessRequestSerializer,
        responses={
            202: openapi.Response(
                description="Task accepted",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'task_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = ProcessRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        task_result = TaskResult.objects.create(
            email=serializer.validated_data['email'],
            message=serializer.validated_data['message']
        )
        process_message.delay(str(task_result.id))  # Send to Celery
        return Response({
            "task_id": str(task_result.id),
            "status": task_result.status
        }, status=status.HTTP_202_ACCEPTED)

class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={
            200: TaskResultSerializer,
            404: "Task not found"
        }
    )
    def get(self, request, task_id):
        try:
            task = TaskResult.objects.get(id=task_id)
            return Response({
                "task_id": str(task.id),
                "status": task.status,
                "result": task.result,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            })
        except TaskResult.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)