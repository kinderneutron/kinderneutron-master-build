import pika
from neo4j import GraphDatabase
import serial
import json
import os

# Neo4j credentials and connection
uri = "neo4j://neo4j-container:7687"
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'


# Arduino serial connection
arduino_port = '/dev/ttyACM0'
arduino_baudrate = 9600
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'RabbitMQ-Server')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')
RABBITMQ_USERNAME = os.getenv('RABBITMQ_DEFAULT_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS', 'admin')
ser = serial.Serial(arduino_port, arduino_baudrate)

def fetch_pin(message):
    query = ''
    with driver.session() as session:
        
        if message['near'] == True and message['far']==False:
            query = (
    "MATCH (camera:Camera)-[:MAPPED_TO]->(area:Near)-[:CONNECTED_TO]->(bulb:Bulb) "
    "WHERE area.name = 'Near' "
    "RETURN collect(bulb.pin) AS pins"
)
        elif message['near'] == False and message['far']==True:
            query = (
    "MATCH (camera:Camera)-[:MAPPED_TO]->(area:Far)-[:CONNECTED_TO]->(bulb:Bulb) "
    "WHERE area.name = 'Far' "
    "RETURN collect(bulb.pin) AS pins"
)
        elif message['near'] == True and message['far']==True:
            query = (
    """
MATCH (camera:Camera)-[:MAPPED_TO]->(area)-[:CONNECTED_TO]->(bulb:Bulb) 
WHERE area.name IN ['Near', 'Far'] 
RETURN collect(bulb.pin) AS pins
"""
)       
        else:
            query = (
    "MATCH (camera:Camera)-[:MAPPED_TO]->(area:NA)-[:CONNECTED_TO]->(bulb:Bulb) "
    "WHERE area.name = 'NA' "
    "RETURN collect(bulb.pin) AS pins"
)      
        result = session.run(query, area_name=message)
        record = result.single().get('pins')
        if record:
            return record
        else:
            return None

def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    print(f"Received message: {message}")
    pin = fetch_pin(message)
    if pin is not None:
        print(f"Sending pin {pin} to Arduino")
        print(str)
        
        ser.write(bytes(str(pin), 'utf-8'))

    else:
        print("Area not found or pin not assigned.")
        ser.write(bytes("L", 'utf-8'))

def consume_messages():
    print(RABBITMQ_HOST)
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    connection_params = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='person_detection')
    channel.basic_consume(queue='person_detection', on_message_callback=callback, auto_ack=True)
    print(f"Waiting for messages from {'person_detection'}. To exit press CTRL+C")
    channel.start_consuming()

    channel = connection.channel()
    channel.queue_declare(queue='person_detection_2')
    channel.basic_consume(queue='person_detection_2', on_message_callback=callback, auto_ack=True)
    print(f"Waiting for messages from {'person_detection_2'}. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_messages()
