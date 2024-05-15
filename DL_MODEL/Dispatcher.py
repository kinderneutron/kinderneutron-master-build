import pika
from neo4j import GraphDatabase
import serial
import json
import threading
import os
timer = None
# Neo4j credentials and connection
uri = "neo4j://neo4j-container:7687"
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))
pin_values = []
pin_values_2 = []
# RabbitMQ connection parameters
rabbitmq_host = 'localhost'

# Arduino serial connection
arduino_port = '/dev/ttyACM0'
arduino_baudrate = 9600
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'RabbitMQ-Server')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')
RABBITMQ_USERNAME = os.getenv('RABBITMQ_DEFAULT_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS', 'admin')
try:
    ser = serial.Serial(arduino_port, arduino_baudrate,timeout=0.2)
except Exception as e:
    print('Warning: Arduino is Not Attached to Your Device')

# Mapping of queue names to pin values
queue_pin_mapping = {
    'person_detection': {'near': [3, 4], 'far': [5]},
    'person_detection_2': {'near': [6], 'far': [7]}
}

# Current active pins across all queues
active_pins = set()

def fetch_pin(message):
    query = ''
    with driver.session() as session:
        if message['near'] == True and message['far'] == False:
            query = (
                """MATCH (camera:Camera)-[:MAPPED_TO]->(area:Near)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name = 'Near' """
                """RETURN collect(bulb.pin) AS pins"""
            )
        elif message['near'] == False and message['far'] == True:
            query = (
                """MATCH (camera:Camera)-[:MAPPED_TO]->(area:Far)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name = 'Far' """
                """RETURN collect(bulb.pin) AS pins"""
            )
        elif message['near'] == True and message['far'] == True:
            query = (
                """MATCH (camera:Camera)-[:MAPPED_TO]->(area)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name IN ['Near', 'Far'] """
                """RETURN collect(bulb.pin) AS pins"""
            )
        else:
            query = (
                """MATCH (camera:Camera)-[:MAPPED_TO]->(area:NA)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name = 'NA' """
                """RETURN collect(bulb.pin) AS pins"""
            )

        result = session.run(query, area_name=message)
        record = result.single().get('pins')
        if record:
            return record
        else:
            return None
def fetch_pin_2(message):
    query = ''
    with driver.session() as session:
        if message['near'] == True and message['far'] == False:
            query = (
                """MATCH (camera:Camera)-[:CONNECTED_TO]->(area:Near)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name = 'near' """
                """RETURN collect(bulb.pin) AS pins"""
            )
        elif message['near'] == False and message['far'] == True:
            query = (
                """MATCH (camera:Camera )-[:CONNECTED_TO]->(area:Far)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name = 'far' """
                """RETURN collect(bulb.pin) AS pins"""
            )
        elif message['near'] == True and message['far'] == True:
            query = (
                """MATCH (camera:Camera)-[:CONNECTED_TO]->(area)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name IN ['Near', 'Far'] """
                """RETURN collect(bulb.pin) AS pins"""
            )
        else:
            query = (
                """MATCH (camera:Camera {name:"camera2"})-[:CONNECTED_TO]->(area:NA)-[:CONNECTED_TO]->(bulb:Bulb) """
                """WHERE area.name = 'NA' """
                """RETURN collect(bulb.pin) AS pins"""
            )

        result = session.run(query, area_name=message)
        record = result.single().get('pins')
        if record:
            return record
        else:
            return None

def update_active_pins(pin_values, add=True):
    global active_pins
    if add:
        active_pins |= set(pin_values)
    else:
        active_pins -= set(pin_values)
    
    return list(active_pins)

def callback(ch, method, properties, body):
    global message,pin_list,timer
    message = json.loads(body.decode('utf-8'))
    print(f"Received message: {message}")
    pin_list = []
    global pin_values,pin_values_2
    # Determine the queue name from which the message originated
    queue_name = method.routing_key
    if queue_name == 'person_detection':
        pin_values = fetch_pin(message)
    elif queue_name == 'person_detection_2': 
        pin_values_2 = fetch_pin_2(message)
    pin_values = [] if pin_values == None else pin_values
    pin_values_2 = [] if pin_values_2 == None else pin_values_2
    # Get the pin values based on the queue name and message content
    #pin_values = queue_pin_mapping.get(queue_name, {}).get(message.get('status', 'near'), [])
    pin_list = pin_values + pin_values_2
    if timer is not None:
        timer.cancel()
        # Set the timer to wait for 2 seconds before sending data
    timer = threading.Timer(1.0, update_arduino)
    timer.start()
    
def update_arduino():
    global message,pin_list
    if pin_list != []:
        # Update the active pins based on the current message
        active_pins_updated = update_active_pins(pin_values, message.get('active', True))
        #print(f"Active pins: {pin_list}")

        # Send the updated active pins to Arduino
        print(f"Sending active pins {pin_list} to Arduino")
        try:
            ser.write(bytes(str(pin_list), 'utf-8'))
            while True:
                if ser.in_waiting > 0:
                    response = ser.readline().decode().strip()
                    if response == "Done":
                        break
        except Exception as e:
            print('Warning: Arduino is Not Attached to Your Device')
    else:
        print("Area not found or pin not assigned.")
        try:
            ser.write(bytes("L", 'utf-8'))
            while True:
                if ser.in_waiting > 0:
                    response = ser.readline().decode().strip()
                    if response == "Done":
                        break
        except Exception as e:
            print('Warning: Arduino is Not Attached to Your Device')
def consume_messages():
    print(RABBITMQ_HOST)
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    connection_params = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    # Declare queues
    channel.queue_declare(queue='person_detection')
    channel.queue_declare(queue='person_detection_2')

    # Set up consumers for each queue
    channel.basic_consume(queue='person_detection', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='person_detection_2', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_messages()
