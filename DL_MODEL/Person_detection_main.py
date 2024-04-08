import cv2
import numpy as np
import requests
import os
import json
import serial

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getUnconnectedOutLayersNames()
ser = serial.Serial('/dev/ttyACM0', 9600)
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.json'))
# Function to process video frames and perform object detection
def process_frame(frame):
    height, width, _ = frame.shape

    # Convert the frame to a blob
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
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

# Main function to process video frames from the HTTP video feed
def process_video_feed(url):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print("Error fetching video feed:", response.status_code)
        return

    bytes_data = bytes()
    for chunk in response.iter_content(chunk_size=10):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # Start of frame
        b = bytes_data.find(b'\xff\xd9')  # End of frame
        if a != -1 and b != -1:
            frame_data = bytes_data[a:b + 2]
            bytes_data = bytes_data[b + 2:]
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Process the frame (perform object detection)
            processed_frame, person_detected = process_frame(frame)

            # Display the processed frame
            #cv2.imshow('Human Detection', processed_frame)

            if person_detected:
                print("Person Detected! Acknowledgement: Present")
                ser.write(b'H')
                jsonupdate('yes')
            else:
                print("Person Not Detected! Acknowledgement: Absent")
                ser.write(b'L')
                jsonupdate('no')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def jsonupdate(val):
    with open(filepath, 'r+') as file:
            data = json.load(file)
            data['person_detected'] = val
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            print("JSON file updated successfully.")
# Example usage

video_feed_url = 'http://kinderneutronapicontainer:8001/videostreamapi'  # Replace with your server URL
process_video_feed(video_feed_url)
cv2.destroyAllWindows()
ser.close() 