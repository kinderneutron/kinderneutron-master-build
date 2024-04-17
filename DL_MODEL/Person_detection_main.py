import asyncio
import cv2
import numpy as np
import requests
import os
import json
import time
import serial
from neo4j import GraphDatabase
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.json'))
uri = "neo4j://neo4j-container:7687"
username = "neo4j"
password = "password"
query = (
        "MATCH (:Camera)-[:CONNECTED_TO]->(bulb:Bulb) "
        "RETURN bulb.pin"
    )
driver = GraphDatabase.driver(uri, auth=(username, password))
from DatabaseUpdate import Database_Update as kinderneutron
# Load YOLO
kn = kinderneutron()
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getUnconnectedOutLayersNames()

# Define global variables
video_feed_url = 'http://kinderneutronapicontainer:8001/videostreamapi'
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.json'))
ser = serial.Serial('/dev/ttyACM0', 9600)
# Distance thresholds for near and far detection (you can adjust these values)
NEAR_DISTANCE_THRESHOLD = 900  # Example threshold for near detection (pixels)
FAR_DISTANCE_THRESHOLD = 50   # Example threshold for far detection (pixels)

# Asynchronous function to process video frames and perform object detection
async def process_frame(frame):
    height, width, _ = frame.shape

    # Convert the frame to a blob
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (218, 218), swapRB=True, crop=False)
    net.setInput(blob)

    # Forward pass through the network
    detections = net.forward(layer_names)

    # Flag and distance to store person detection and distance information
    person_detected = False
    distance_to_person = None

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

                # Calculate distance based on bounding box size (you may need calibration for accurate distance estimation)
                box_size = max(w, h)
                if 450 <box_size <= NEAR_DISTANCE_THRESHOLD:
                    distance_to_person = 'near'
                elif 450>=box_size >= FAR_DISTANCE_THRESHOLD:
                    distance_to_person = 'far'
                else:
                    distance_to_person = 'unknown'

                # Draw a bounding box around the person
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                person_detected = True

    return frame, person_detected, distance_to_person

# Asynchronous function to fetch and process video frames
async def process_video_feed_async(url):
    flag = ''
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
            processed_frame, person_detected, distance = await process_frame(frame)

            # Handle the processed frame (e.g., display, save to file)
            if person_detected:
                if distance == 'near':
                    if flag != 'near':
                        print("Person Detected Near Camera")
                        bulbs_pins = fetch_bulb_pins('near')
                        print(bulbs_pins)
                        ser.write(bytes(str(bulbs_pins), 'utf-8'))
                        flag = 'near'
                        jsonupdate(bulbs_pins)
                    # Perform actions for near detection
                elif distance == 'far':
                    if flag != 'far':
                        print("Person Detected Far from Camera")
                        bulbs_pins = fetch_bulb_pins('far')
                        print(bulbs_pins)
                        flag = 'far'
                        ser.write(bytes(str(bulbs_pins), 'utf-8'))

                        jsonupdate(bulbs_pins)
                else:
                    print("Person Detected (Distance Unknown)")
                    # Perform actions for unknown distance detection
            else:
                print("Person Not Detected")
                jsonupdate([])
                ser.write(bytes('', 'utf-8'))



def fetch_bulb_pins(location):
    
    with driver.session() as session:
        if location.lower() == "near":
            query = (
                "MATCH (:Near)-[:CONNECTED_TO]->(bulb:Bulb) "
                "RETURN bulb.name AS bulb_name, bulb.pin AS bulb_pin"
            )
        elif location.lower() == "far":
            query = (
                "MATCH (:Far)-[:CONNECTED_TO]->(bulb:Bulb) "
                "RETURN bulb.name AS bulb_name, bulb.pin AS bulb_pin"
            )
        else:
            return "Invalid location parameter. Use 'near' or 'far'."

        result = session.run(query)
        bulbs = [(record["bulb_name"], record["bulb_pin"]) for record in result]
        ans = []
        for i in bulbs:
            ans.append(i[1])
        return ans
        
def jsonupdate(val):
    with open(filepath, 'r+') as file:
            data = json.load(file)
            data['pins'] = val
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            print("JSON file updated successfully.")

async def main():
    # Create tasks for asynchronous processing
    tasks = [process_video_feed_async(video_feed_url) for _ in range(4)]  # Create 4 tasks

    # Run tasks concurrently using asyncio.gather()
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    while True:
        asyncio.run(main())  # Run the main coroutine asynchronously

