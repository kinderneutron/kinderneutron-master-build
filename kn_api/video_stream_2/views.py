import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import threading
import time

cap = cv2.VideoCapture(3)

# Function to read frames from camera and stream as HTTP response
def video_stream_2():
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# Decorator to compress the stream using gzip
@gzip.gzip_page
def video_feed_2(request):
    response = StreamingHttpResponse(video_stream_2(), content_type='multipart/x-mixed-replace; boundary=frame')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept'
    return response

# Start the camera capture in a separate thread
def start_camera_capture():
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(1)  # Wait for camera to initialize
    threading.Thread(target=video_feed_2).start()

start_camera_capture()  # Start camera capture when server starts