from celery import Celery

# Define the Celery application
app = Celery('tasks', broker='redis://localhost:6379/0')

# Configuration options (optional)
app.conf.update(
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)
