# tasks.py

from celery import Celery
import subprocess
import time
app = Celery('tasks',  broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')  # Update with your app name

@app.task
def start_container():
    # Command to execute Docker container
    command = 'docker exec -it kinderneutroncontainr'

    # Execute the Docker command using subprocess
    try:
        subprocess.run([
            "gnome-terminal","--tab","--", "bash",  "-c", 
            "docker exec -it kinderneutronapicontainer bash -c 'cd kn_api/&& exec bash -c \"python3 manage.py runserver 0:8001\"& exec bash'"
        ])
     
        subprocess.run([
            "gnome-terminal", "--", "bash","-c", 
            "docker exec -it kinderneutroncontainer bash -c 'cd webapp/&& exec bash -c \"python3 manage.py runserver 0:8000\"& exec bash'"
        ])
        time.sleep(5)
        subprocess.run([
            "gnome-terminal", "--tab","--", "bash", "-c", 
            "docker exec -it kinderneutroncontainer bash -c 'cd DL_MODEL/&& exec bash -c \"python3 Person_detection_main.py\"& exec bash'"
        ])
        # subprocess.run([
        #     "gnome-terminal", "--tab" "--", "bash", "-c" 
        #     "docker exec -it psql-db sh -c "
        # ])
        return 'Container started successfully.'

    except subprocess.CalledProcessError as e:
        return f'Error starting container: {e}'
