from tasks import start_container

# Call the Celery task asynchronously
result = start_container.delay()

# Retrieve the result (this will block until the task is complete)
print(result.get())
