import asyncio
import cv2
import numpy as np
import requests
import os
import json
import time
from DatabaseUpdate import Database_Update as kinderneutron

# Load YOLO
kn = kinderneutron()
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getUnconnectedOutLayersNames()

# Define global variables
video_feed_url = 'http://kinderneutronapicontainer:8001/videostreamapi'
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.json'))

# Asynchronous function to process video frames and perform object detection
async def process_frame(frame):
    height, width, _ = frame.shape

    # Convert the frame to a blob
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (218, 218), swapRB=True, crop=False)
    net.setInput(blob)

    # Forward pass through the network
    detections = net.forward(layer_names)

    # Flag to check if a person is detected
    person_detected = False

    # Process the detections
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and class_id == 0:  # Class ID 0 represents a person in COCO dataset
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)

                # Draw a bounding box around the person
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                person_detected = True

    return frame, person_detected

# Asynchronous function to fetch and process video frames
async def process_video_feed_async(url):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print("Error fetching video feed:", response.status_code)
        return

    bytes_data = bytes()
    for chunk in response.iter_content(chunk_size=100):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # Start of frame
        b = bytes_data.find(b'\xff\xd9')  # End of frame
        if a != -1 and b != -1:
            frame_data = bytes_data[a:b + 2]
            bytes_data = bytes_data[b + 2:]
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            # Process the frame asynchronously (perform object detection)
            processed_frame, person_detected = await process_frame(frame)

            # Handle the processed frame (e.g., display, save to file)
            if person_detected:
                
                # ser.write(b'H')
                if checkjson() == 'no':
                    print("Person Detected! Acknowledgement: Present")
                    jsonupdate('yes')
                    kn.dbupdate()
            else:
                
                # ser.write(b'L')
                if checkjson() == 'yes':
                    print("Person Not Detected")
                    jsonupdate('no')
                    kn.dbupdate()
                # Perform actions based on detection
async def main():
    # Create tasks for asynchronous processing
    tasks = [process_video_feed_async(video_feed_url) for _ in range(4)]  # Create 4 tasks

    # Run tasks concurrently using asyncio.gather()
    await asyncio.gather(*tasks)
def jsonupdate(val):
    with open(filepath, 'r+') as file:
            data = json.load(file)
            data['person_detected'] = val
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            print("JSON file updated successfully.")
def checkjson():
    with open(filepath, 'r+') as file:
            data = json.load(file)
            return data['person_detected']
if __name__ == "__main__":
    while True:
        asyncio.run(main())  # Run the main coroutine asynchronously
