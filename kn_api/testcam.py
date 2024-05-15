import cv2

def test_camera(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return False
    cap.release()
    return True

def list_available_cameras():
    index = 0
    available_cameras = []
    while True:
        if test_camera(index):
            available_cameras.append(index)
            index += 1
        else:
            break
    return available_cameras

# List all available cameras
cameras = list_available_cameras()
print("Available Cameras:", cameras)
