from django.conf import settings

# Configure Celery to run tasks synchronously for testing
settings.CELERY_TASK_ALWAYS_EAGER = True
settings.CELERY_TASK_EAGER_PROPAGATES = True