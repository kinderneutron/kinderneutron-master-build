# tasks.py

from celery import Celery
import subprocess
import time
app = Celery('tasks',  broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')  # Update with your app name

@app.task
def start_container():
    # Command to execute Docker container
    command = 'docker exec -it kinderneutroncontainr'
    print("Starting Kinderneutron Container Now:")
    # Execute the Docker command using subprocess
    try:
        subprocess.run([
            "gnome-terminal","--tab","--", "bash",  "-c", 
            "docker exec -it kinderneutronapicontainer bash -c 'cd kn_api/&& exec bash -c \"python3 manage.py runserver 0:8001\"& exec bash'"
        ])
        print("API Containers Are Up")
        subprocess.run([
            "gnome-terminal", "--", "bash","-c", 
            "docker exec -it kinderneutroncontainer bash -c 'cd webapp/&& exec bash -c \"python3 manage.py runserver 0:8000\"& exec bash'"
        ])
        print("Webapp is Up")
        time.sleep(3)
        subprocess.run([
            "gnome-terminal", "--tab","--", "bash", "-c", 
            "docker exec -it kinderneutroncontainer bash -c 'cd DL_MODEL/&& exec bash -c \"python3 Person_detection_main.py\"& exec bash'"
        ])
        print("KN2.0 Model Has Started Detecting")
        subprocess.run([
            "gnome-terminal", "--tab","--", "bash", "-c", 
            "docker exec -it kinderneutroncontainer bash -c 'cd DL_MODEL/&& exec bash -c \"python3 Dispatcher.py\"& exec bash'"
        ])
        print('Dispatcher Script is Running')
        time.sleep(3)
        # subprocess.run([
        #     "gnome-terminal", "--tab" "--", "bash", "-c" 
        #     "docker exec -it psql-db sh -c "
        # ])
        return 'Kinderneuron Architecture has Started successfully.'

    except subprocess.CalledProcessError as e:
        return f'Error starting Kinderneutron Container : {e}'
