import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import threading
import time

cap = cv2.VideoCapture(0)

# Function to read frames from camera and stream as HTTP response
def video_stream():
    while True:
        success, frame = cap.read()
        if not success:
            print("Error reading frame from camera")
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# Decorator to compress the stream using gzip
@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')

# Start the camera capture in a separate thread
def start_camera_capture():
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(1)  # Wait for camera to initialize
    threading.Thread(target=video_feed).start()

# Reconnect logic for camera
def reconnect_camera():
    global cap
    cap.release()
    cap = cv2.VideoCapture(0)
    start_camera_capture()

# Main function to start camera capture and handle errors
def main():
    start_camera_capture()  # Start camera capture when server starts
    while True:
        try:
            time.sleep(1)  # Check every second
            if not cap.isOpened():
                print("Camera not opened, reconnecting...")
                reconnect_camera()
        except Exception as e:
            print("Exception occurred:", e)
            print("Reconnecting...")
            reconnect_camera()

if __name__ == "__main__":
    main()
