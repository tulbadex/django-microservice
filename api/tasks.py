from celery import shared_task
from .models import TaskResult, TaskStatus
from time import sleep

@shared_task(bind=True, name="api.tasks.process_message")
def process_message(self, task_id):
    print(f"Processing task: {task_id}")
    try:
        task = TaskResult.objects.get(id=task_id)
        task.status = TaskStatus.PROCESSING
        task.save()

        # Simulate processing time
        sleep(10)

        result_data = {
            "processed_message": task.message.upper(),
            "email": task.email,
        }

        task.result = result_data
        task.status = TaskStatus.COMPLETED
        task.save()
        return result_data
    except TaskResult.DoesNotExist:
        return {"error": "Task not found"}
    except Exception as e:
        task.status = TaskStatus.FAILED
        task.result = {"error": str(e)}
        task.save()
        raise e